import asyncio
import datetime
import os


import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SEARCH_TOKEN = " mrAgentWebSearch=true ,"
SCRAPE_TOKEN = " mrAgentScrape=true ,"
EMAIL_TOKEN = " mrAgentSendEmail=true ,"

# === Session-state defaults ===#
for key, default in [
    ("message", ""),
    ("response_raw", ""),
    ("response_display", ""),
    ("tool_events", []),
    ("search_on", False),
    ("scrape_on", False),
    ("email_on", False),
]:
    st.session_state.setdefault(key, default)


class ToolUsageLogger(BaseCallbackHandler):
    def __init__(self):
        self.eventsToolStart: dict[str, int] = {}

    async def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        name = serialized.get("name", "<unknown>")
        if name == "web_search":
            key = f"Seaching the web for: {input_str[11:-2]}"
            print("added this ", key)
            self.eventsToolStart[key] = 0
            st.session_state["tool_events"].append(key)
        elif name == "scrape_website":
            key = f"Running scrape({input_str[9:-2]})"
            print("added this ", key)
            self.eventsToolStart[key] = 0
            st.session_state["tool_events"].append(key)
        elif name == "send_email":
            print(input_str)
            key = "Sending Email"
            print("added this ", key)
            self.eventsToolStart[key] = 0
            st.session_state["tool_events"].append(key)

    async def on_tool_end(self, output, **kwargs):
        for event in self.eventsToolStart:
            if event in output:
                self.eventsToolStart.pop(event)
                print("removed this ", event)
                break


def run_mcp_client(message: str) -> str:

    # logger = StdOutCallbackHandler()
    logger = ToolUsageLogger()

    async def _main(msg: str) -> str:
        server_params = StdioServerParameters(
            command="python",
            args=["C:/Users/user/Desktop/eya_agent/ai-agent/server.py"],
        )

        async with stdio_client(server_params) as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)

                def filter_tools(text):
                    allowed = set()
                    if "mrAgentWebSearch=true" in text:
                        allowed.add("web_search")
                    if "mrAgentScrape=true" in text:
                        allowed.add("scrape_website")
                    if "mrAgentSendEmail=true" in text:
                        allowed.add("send_email")
                        allowed.add("read_emails")

                    return [t for t in tools if t.name in allowed]

                filtered = filter_tools(msg)
                # handlers = [ logger]
                llm = ChatGoogleGenerativeAI(
                    api_key=os.getenv("GEMINI_API_KEY"),
                    model="gemini-2.0-flash",
                    disable_streaming=False,
                )
                system = f"Today is {datetime.datetime.now():%Y-%m-%d}"
                agent = create_react_agent(llm, filtered)
                # config = {"callbacks": [logger]}
                res = await agent.ainvoke(
                    {
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": msg},
                        ],
                    },
                    {"callbacks": [logger]},
                )
                print("events", logger.eventsToolStart)
                return res

    return asyncio.run(_main(message))
    # portal = BlockingPortal()
    # response = portal.call(_main, message)
    # return response


st.title("agent aye")

st.session_state["message"] = st.text_area(
    "Enter your message:", value=st.session_state["message"], height=150
)

# Toggles — note keys match the session_state names
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.checkbox("🔍 Search", key="search_on")
with col2:
    st.checkbox("🕷️ Scrape", key="scrape_on")
with col3:
    st.checkbox("✉️ Email", key="email_on")

if col4.button("Submit"):
    prompt = st.session_state["message"]
    st.session_state["tool_events"] = []
    if st.session_state["search_on"]:
        prompt += SEARCH_TOKEN
    if st.session_state["scrape_on"]:
        prompt += SCRAPE_TOKEN
    if st.session_state["email_on"]:
        prompt += EMAIL_TOKEN

    # placeholder = st.empty()

    # def worker():
    #     result = run_mcp_client(prompt)
    #     st.session_state["response_raw"] = result
    #     messages = result.get("messages", [])
    #     content = ""
    #     for msg in reversed(messages):
    #         if isinstance(msg, AIMessage) or hasattr(msg, "content"):
    #             content = msg.content
    #             break
    #     st.session_state["response_display"] = content
    #
    # thread = threading.Thread(target=worker, daemon=True)
    # thread.start()

    with st.spinner("Thinking..."):
        # while thread.is_alive():
        #     lines = []
        #     for evt in st.session_state["tool_events"]:
        #         lines.append(evt if len(evt) <= 60 else evt[:60] + "…")
        #     placeholder.text("\n".join(lines) or "Waiting for tools…")
        #     time.sleep(0.1)

        result = run_mcp_client(prompt)
        st.session_state["response_raw"] = result
        messages = result.get("messages", [])
        content = ""
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) or hasattr(msg, "content"):
                content = msg.content
                break
        st.session_state["response_display"] = content
    # placeholder.empty()

st.markdown("---")

st.subheader("Tool Usage")

if st.session_state["tool_events"]:
    for evt in st.session_state["tool_events"]:
        st.write(f"• {evt}")
else:
    st.write("(No tools invoked yet)")

st.subheader("Response")
if st.session_state["response_display"]:
    st.write(st.session_state["response_display"])
    print(st.session_state["response_display"])
else:
    st.info("No response yet — type a message and click **Submit**.")

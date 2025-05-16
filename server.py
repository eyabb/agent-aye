import os
import pickle
import base64

from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from langchain_community.utilities import SerpAPIWrapper
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

# serpapi_api_key=os.getenv("SERPAPI_API_KEY")
searcher = SerpAPIWrapper(
    serpapi_api_key="066ae1bdd61da9919d58036f3d6d8475b98d072d09a66dfbbbc6617dc1a6e9f1"
)


# @mcp.tool()
# def add(a: int, b: int) -> dict:
#     result = a + b
#     return {
#         "status": f" Running add({a}, {b})",
#         "value": result
#     }

@mcp.tool()
def read_emails(query: str = "is:unread", max_results: int = 1) -> dict:
    """
    Search your Gmail inbox and return up to `max_results` snippets.
    `query` follows Gmail’s search syntax (e.g. 'label:INBOX is:unread').
    """
    service = get_gmail_service()
    # 1) List message IDs matching the query
    resp = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()  # :contentReference[oaicite:3]{index=3}

    messages = []
    for m in resp.get("messages", []):
        # 2) Fetch full message for each ID
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="full"
        ).execute()  # :contentReference[oaicite:4]{index=4}

        # 3) Extract a snippet (or dig into payload for body)
        snippet = msg.get("snippet", "")  # :contentReference[oaicite:5]{index=5}
        messages.append({"id": m["id"], "snippet": snippet})

    return {
        "status": f"Retrieved {len(messages)} messages matching '{query}'",
        "value": messages
    }

@mcp.tool()
async def scrape_website(url: str) -> dict:
    SCROLL_TO_LOAD_EVERYTHING_IF_LAZY_LOADED = True
    config = CrawlerRunConfig(
        scan_full_page=SCROLL_TO_LOAD_EVERYTHING_IF_LAZY_LOADED,
        scroll_delay=0.5,
        cache_mode=CacheMode.BYPASS,
        exclude_all_images=True,
        excluded_tags=['form', 'header', 'footer', 'nav'],
        )

    async with AsyncWebCrawler(headless=True) as crawler:
        result = await crawler.arun(url=url, config=config)

    return {

        "status": f" Running scrape({url})",
        "value": result.cleaned_html
    }


# @mcp.tool()
# def multiply(a: int, b: int) -> dict:
#     result = a * b
#     return {
#         "status": f" Running multiply({a}, {b})",
#         "value": result
#     }


@mcp.tool()
def web_search(query: str) -> dict:
    searchResult = searcher.run(query)
    return {
        "status": f" Searching the web for: {query}",
        "value": searchResult
    }


def get_gmail_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as f:
            creds = pickle.load(f)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)


@mcp.tool()
def send_email(to: str, subject: str, body: str) -> dict:
    service = get_gmail_service()
    msg = MIMEText(body)
    msg["to"] = to
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return {"status": f" Sent email to {to}", "value": sent.get("id")}


if __name__ == "__main__":
    mcp.run(transport="stdio")

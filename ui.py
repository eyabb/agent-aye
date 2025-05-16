import streamlit as st

SEARCH_TOKEN = " mrAgentSearch ,"
SCRAPE_TOKEN = " mrAgentScrape ,"
EMAIL_TOKEN = " mrAgentSendEmail ,"

if 'message' not in st.session_state:
    st.session_state['message'] = ''

if 'response' not in st.session_state:
    st.session_state['response'] = ''

st.title("agent aye")

st.session_state['message'] = st.text_area(
    "Enter your message:",
    value=st.session_state['message'],
    key='prompt_input'
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Search"):
        st.session_state['message'] += f" {SEARCH_TOKEN}"
with col2:
    if st.button("Scrape"):
        st.session_state['message'] += f" {SCRAPE_TOKEN}"
with col3:
    if st.button("Send Email"):
        st.session_state['message'] += f" {EMAIL_TOKEN}"
with col4:
    if st.button("Submit"):
        with st.spinner("Sending to MCP client..."):
            print("hello")

with st.container():
    st.subheader("Response")
    if st.session_state['response']:
        st.write(st.session_state['response'])
    else:
        st.write("How can I help you today? ")
# st.subheader("Final Message Prompt")
# st.write(st.session_state['message'])

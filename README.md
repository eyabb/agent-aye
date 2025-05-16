 agent-aye
============

A Streamlit + MCP-based chatbot with web-search, scraping, email send/read tools.

* * *

Step 0: Clone the Repository
----------------------------

    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    

Step 1: Install Universal Venv (`uv`)
-------------------------------------

    pipx install uv

Step 2: Activate the Virtual Environment
----------------------------------------

Navigate to the project root and run:

*   **Linux / macOS**  
    `source .venv/bin/activate`
*   **Windows (PowerShell)**  
    `.venv\Scripts\Activate.ps1`

Step 3: Install Dependencies
----------------------------

    uv sync

Step 4: Set Your Gemini API Key
-------------------------------

    export GEMINI_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"

> **Windows (PowerShell):**  
> `$Env:GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"`

Step 5: Run the MCP Server
--------------------------

    python server.py

Step 6: Enable Gmail API & Generate OAuth Credentials
-----------------------------------------------------

1.  Visit the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create/select a project, enable the Gmail API.
3.  Configure OAuth consent and create an OAuth Client ID.

Step 7: Place & Rename Your Credentials JSON
--------------------------------------------

Download the OAuth client JSON, rename it to `credentials.json`, and move it into the project root.

Step 8: Run OAuth Setup
-----------------------

    python oauth_setup.py

Follow the browser prompts to grant scopes and save `token.pickle`.

Step 9: Launch the Streamlit UI
-------------------------------

In a new terminal, repeat **Steps 2–5**, then:

    streamlit run client-with-ui.py

Step 10: Enjoy!
---------------

Use the **Search**, **Scrape**, **Send Email**, and **Read Emails** toggles, click **Submit**, and watch tool-invocation events stream.

### Notes

*   **Date Override:** We reset Gemini’s system date to today, through a system prompt, to play around the safety limitation rule that gemini is imposing; it stops the scrapping of websites that have dates in their url superior than the current date and since the perceived date of gemini is amid 2023, this won't let us scrape any up-to-date websites that their dates are part of their urls, i.e. most blogs and news articles. But after resetting the clock we bypassed that limitation.
*   **Secret Management:** Dealt with sensible secrets with delicacy, not pushing them to git so that they don't get leaked, the only exception to that was SerpAPI key where I had to be pragmatic, cause at first it wasn't that sensible and also I had to deal with the subprocess pain to pass it as an environmental variable which wasn't worth it, considering that I had other more important priorities.
*   **Agent Architecture:** I used a single agent architecture, because it is the simplest and the time is limited, however if I were to use another architecture I would have used the parallel agent one, it would be very useful for sending a bulk of emails with minimal latency and doing independent searches, that being said the agent is just for this take home test purpose and isn't going to be used for a production heavy environment, so that would be over-engineering and the single architecture does the trick. 

  Project Readme body { font-family: Arial, sans-serif; line-height: 1.6; margin: 2rem; } h1, h2, h3 { color: #333; } code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; } pre { background: #f4f4f4; padding: 1rem; border-radius: 4px; overflow-x: auto; } blockquote { border-left: 4px solid #ccc; padding-left: 1rem; color: #666; }

Project Name
============

A Streamlit + MCP-based chatbot with web-search, scraping, email send/read tools.

* * *

Step 0: Clone the Repository
----------------------------

    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    

Step 1: Install Universal Venv (`uv`)
-------------------------------------

    pip install universal-venv

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

Use the **Search**, **Scrape**, **Send Email**, and **Read Emails** toggles, click **Submit**, and watch tool-invocation events stream live.

### Notes & Caveats

*   **Date Override:** We reset Gemini’s system date to today to avoid scraping blocks on URLs dated past mid-2023.
*   **Secret Management:** SerpAPI key is in plaintext for simplicity; for production, store securely.
*   **Agent Architecture:** Single-agent design chosen for brevity; a parallel-agent setup would improve bulk-email latency but isn’t necessary here.

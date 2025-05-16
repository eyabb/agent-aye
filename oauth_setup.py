# oauth_setup.py
import os, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly"]
CREDS_JSON = "credentials.json"   # rename your downloaded JSON to this
TOKEN_PKL   = "token.pickle"

def authorize_gmail():
    creds = None
    # 1) Load existing tokens if present
    if os.path.exists(TOKEN_PKL):
        with open(TOKEN_PKL, "rb") as f:
            creds = pickle.load(f)
    # 2) If no valid creds, run local server flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_JSON, SCOPES)
            # This spins up http://localhost:8000 by default (matching your javascript_origin)
            creds = flow.run_local_server(port=8000)
        # 3) Persist for reuse
        with open(TOKEN_PKL, "wb") as f:
            pickle.dump(creds, f)
    return creds

if __name__ == "__main__":
    authorize_gmail()


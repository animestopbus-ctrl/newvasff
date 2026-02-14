import requests
import os

def fetch_github_data(username):
    url = f"https://api.github.com/users/{username}"
    
    # GitHub requires a User-Agent header so they know who is calling
    headers = {
        "User-Agent": "Telegram-GitHub-Bot-LastPerson07",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # If you add a GITHUB_TOKEN to Render, this will unlock 5,000 requests/hour!
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        res = requests.get(url, headers=headers)
        data = res.json()

        # 200 means SUCCESS!
        if res.status_code == 200:
            return data
            
        # 404 means the user literally does not exist
        elif res.status_code == 404:
            return {"error": f"❌ GitHub user <b>{username}</b> not found."}
            
        # Anything else (like 403) means Rate Limit or blocked!
        else:
            error_msg = data.get("message", "Unknown error from GitHub")
            return {"error": f"⚠️ <b>GitHub API Error:</b> {error_msg}\n\n<i>(To fix this, add a GITHUB_TOKEN in your Render Environment Variables!)</i>"}

    except Exception as e:
        print(f"API Error: {e}")
        return {"error": "⚠️ Failed to connect to GitHub. Try again later."}

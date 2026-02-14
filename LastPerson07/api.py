import requests
import os

def fetch_github_data(username):
    url = f"https://api.github.com/users/{username}"
    
    # This tells GitHub we are a real bot, not a spammer
    headers = {
        "User-Agent": "Telegram-GitHub-Bot-LastPerson07",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # This grabs the token you just put into Render!
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        res = requests.get(url, headers=headers)
        data = res.json()

        # 200 means PERFECT SUCCESS!
        if res.status_code == 200:
            return data
            
        # 404 means the user literally does not exist
        elif res.status_code == 404:
            return {"error": f"❌ GitHub user <b>{username}</b> not found."}
            
        # This catches the Rate Limit error so it doesn't print N/A!
        else:
            error_msg = data.get("message", "Unknown error from GitHub")
            return {"error": f"⚠️ <b>GitHub Blocked Us:</b> {error_msg}\n\n<i>Make sure your GITHUB_TOKEN is correct in Render!</i>"}

    except Exception as e:
        print(f"API Error: {e}")
        return {"error": "⚠️ Failed to connect to GitHub. Try again later."}

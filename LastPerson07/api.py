import requests

def fetch_github_data(username):
    url = f"https://api.github.com/users/{username}"
    try:
        res = requests.get(url)
        data = res.json()

        if "message" in data and data["message"] == "Not Found":
            return {"error": f"❌ GitHub user <b>{username}</b> not found."}

        return data
    except Exception as e:
        print(f"API Error: {e}")
        return {"error": "⚠️ Failed to fetch GitHub profile. Try again later."}

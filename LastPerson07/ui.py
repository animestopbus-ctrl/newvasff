import html

def safe_html(text, default="N/A"):
    """Cleans text so symbols like < or > don't crash Telegram's HTML parser."""
    if not text or text == "None":
        return default
    return html.escape(str(text))

def format_profile_text(data):
    # Extract and safely escape all text fields
    name = safe_html(data.get("name"))
    login = safe_html(data.get("login"))
    id_ = safe_html(data.get("id"))
    node_id = safe_html(data.get("node_id"))
    location = safe_html(data.get("location"))
    company = safe_html(data.get("company"))
    blog = safe_html(data.get("blog"))
    email = safe_html(data.get("email"))
    hireable = safe_html(data.get("hireable"))
    twitter = safe_html(data.get("twitter_username"))
    bio = safe_html(data.get("bio"), "No bio provided.")
    created = safe_html(data.get("created_at"))
    updated = safe_html(data.get("updated_at"))

    # URLs don't need escaping, just default to empty strings
    html_url = data.get("html_url") or ""
    repos_url = data.get("repos_url") or ""
    followers_url = data.get("followers_url") or ""
    following_url = data.get("following_url") or ""
    gists_url = data.get("gists_url") or ""
    
    # Numbers
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    public_repos = data.get("public_repos", 0)
    public_gists = data.get("public_gists", 0)

    # Format message
    text = (
        f"<b>👤 GitHub Profile</b>\n"
        f"👨‍💻 Name: <b>{name}</b>\n"
        f"🔑 Username: <code>{login}</code>\n"
        f"🆔 ID: <code>{id_}</code>\n"
        f"🧬 Node ID: <code>{node_id}</code>\n"
        f"📍 Location: {location}\n"
        f"🏢 Company: {company}\n"
        f"📰 Blog: {blog}\n"
        f"✉️ Email: {email}\n"
        f"📌 Hireable: {hireable}\n"
        f"🐦 Twitter: {twitter}\n"
        f"📦 Public Repos: <b>{public_repos}</b>\n"
        f"🗃️ Gists: <b>{public_gists}</b>\n"
        f"👥 Followers: <b>{followers}</b> | Following: <b>{following}</b>\n"
        f"📝 Bio: <i>{bio}</i>\n"
        f"📅 Created: {created}\n"
        f"🛠️ Updated: {updated}\n"
        f"🔗 Profile: <a href='{html_url}'>{html_url}</a>\n"
        f"📁 Repos: <a href='{repos_url}'>Repos Link</a>\n"
        f"👤 Followers: <a href='{followers_url}'>Followers</a>\n"
        f"➡️ Following: <a href='{following_url}'>Following</a>\n"
        f"📑 Gists: <a href='{gists_url}'>Gists</a>"
    )
    return text

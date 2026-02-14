import html

def safe_html(text, default="N/A"):
    """Cleans text so symbols like < or > don't crash Telegram's HTML parser."""
    if not text or text == "None":
        return default
    return html.escape(str(text))

def format_profile_text(data):
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
    
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    public_repos = data.get("public_repos", 0)
    public_gists = data.get("public_gists", 0)

    # Format message (Notice we removed the ugly links at the bottom!)
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
        f"🛠️ Updated: {updated}"
    )
    return text

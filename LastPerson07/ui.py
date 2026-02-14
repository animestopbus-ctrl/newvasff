def format_profile_text(data):
    # Extract all fields
    name = data.get("name") or "N/A"
    login = data.get("login") or "N/A"
    id_ = data.get("id") or "N/A"
    node_id = data.get("node_id") or "N/A"
    html_url = data.get("html_url") or ""
    repos_url = data.get("repos_url") or ""
    followers_url = data.get("followers_url") or ""
    following_url = data.get("following_url") or ""
    gists_url = data.get("gists_url") or ""
    blog = data.get("blog") or "N/A"
    location = data.get("location") or "N/A"
    email = data.get("email") or "N/A"
    hireable = str(data.get("hireable")) or "N/A"
    bio = data.get("bio") or "No bio provided."
    twitter = data.get("twitter_username") or "N/A"
    company = data.get("company") or "N/A"
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    public_repos = data.get("public_repos", 0)
    public_gists = data.get("public_gists", 0)
    created = data.get("created_at") or "N/A"
    updated = data.get("updated_at") or "N/A"

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

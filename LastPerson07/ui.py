from typing import Dict, Tuple
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class LastPerson07UI:
    def __init__(self) -> None:
        self.emojis: Dict[str, str] = {
            "profile": "👤",
            "name": "✨",
            "username": "🔑", 
            "id": "🆔",
            "location": "📍",
            "company": "🏢",
            "blog": "🌐",
            "email": "📧",
            "hireable": "💼",
            "twitter": "🐦",
            "repos": "📦",
            "gists": "🗃️",
            "followers": "👥",
            "following": "➡️",
            "bio": "📝",
            "created": "🕐",
            "updated": "🔄",
            "link": "🔗"
        }
    
    def format_date(self, date_str: str) -> str:
        """Format ISO date to readable format"""
        match date_str:
            case "N/A" | "" | None:
                return "N/A"
            case _:
                try:
                    date_obj: datetime = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    return date_obj.strftime("%d %b %Y")
                except ValueError:
                    return date_str
    
    def create_profile_message(self, data: Dict) -> Tuple[str, str]:
        """Create formatted profile message"""
        # Extract and sanitize data
        name = data.get("name") or "N/A"
        login = data.get("login") or "N/A"
        id_ = data.get("id") or "N/A"
        avatar_url = data.get("avatar_url") or ""
        html_url = data.get("html_url") or ""
        blog = data.get("blog") or "N/A"
        location = data.get("location") or "N/A"
        company = data.get("company") or "N/A"
        email = data.get("email") or "N/A"
        hireable = "✅" if data.get("hireable") else "❌"
        twitter = data.get("twitter_username") or "N/A"
        bio = data.get("bio") or "No bio provided."
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        public_repos = data.get("public_repos", 0)
        public_gists = data.get("public_gists", 0)
        created_at = self.format_date(data.get("created_at") or "N/A")
        updated_at = self.format_date(data.get("updated_at") or "N/A")
        
        # Create formatted message
        text = f"""
{self.emojis['profile']} <b>GitHub Profile Explorer</b>
        
{self.emojis['name']} <b>{name}</b> <i>(@{login})</i>

{self.emojis['bio']} <i>"{bio}"</i>

📊 <b>GitHub Stats:</b>
{self.emojis['repos']} Repositories: <b>{public_repos}</b>
{self.emojis['gists']} Gists: <b>{public_gists}</b>
{self.emojis['followers']} Followers: <b>{followers}</b> | {self.emojis['following']} Following: <b>{following}</b>

👤 <b>Profile Information:</b>
{self.emojis['id']} ID: <code>{id_}</code>
{self.emojis['location']} Location: {location}
{self.emojis['company']} Company: {company}
{self.emojis['email']} Email: {email}
{self.emojis['hireable']} Hireable: {hireable}
{self.emojis['twitter']} Twitter: {twitter}
{self.emojis['blog']} Blog: {blog}

📅 <b>Account Timeline:</b>
{self.emojis['created']} Created: {created_at}
{self.emojis['updated']} Updated: {updated_at}

{self.emojis['link']} <a href='{html_url}'>View on GitHub</a>
        """.strip()
        
        return avatar_url, text
    
    def create_profile_buttons(self, data: Dict) -> InlineKeyboardMarkup:
        """Create interactive buttons for GitHub profile"""
        login = data.get("login", "")
        html_url = data.get("html_url", "")
        repos_url = data.get("repos_url", "")
        followers_url = data.get("followers_url", "")
        
        markup = InlineKeyboardMarkup()
        
        # Row 1: Main actions
        markup.row(
            InlineKeyboardButton("🌟 View Profile", url=html_url),
            InlineKeyboardButton("📂 Repositories", url=repos_url)
        )
        
        # Row 2: Additional actions
        markup.row(
            InlineKeyboardButton("👥 Followers", url=followers_url),
            InlineKeyboardButton("🔥 Premium", callback_data=f"github_premium_{login}")
        )
        
        # Row 3: Refresh
        markup.row(
            InlineKeyboardButton("🔄 Refresh Data", callback_data=f"github_refresh_{login}")
        )
        
        return markup
    
    def create_error_message(self, error_type: str, username: str = "") -> str:
        """Create formatted error messages"""
        error_templates = {
            "no_params": """
❌ <b>Missing Username</b>

Please provide a GitHub username after the command.

💡 <b>Example:</b>
<code>/github rahul</code>
<code>/github torvalds</code>
            """,
            "invalid_username": f"""
❌ <b>Invalid Username</b>

The username <b>@{username}</b> doesn't seem to be valid.

🔍 <b>Tips:</b>
• Usernames can only contain alphanumeric characters and hyphens
• Must be between 1-39 characters long
• Check for typos
            """,
            "user_not_found": f"""
❌ <b>User Not Found</b>

GitHub user <b>@{username}</b> was not found.

🤔 <b>Possible reasons:</b>
• User doesn't exist
• Account might be suspended
• Typo in the username
            """,
            "rate_limit": """
⏳ <b>Rate Limit Exceeded</b>

GitHub API rate limit has been reached.

🕐 Please wait a while and try again later.
            """,
            "timeout": """
⏰ <b>Request Timeout</b>

The request took too long to complete.

🌐 Please check your connection and try again.
            """,
            "general_error": """
⚠️ <b>Unexpected Error</b>

Something went wrong while fetching the profile.

🔧 Please try again in a few moments.
            """
        }
        
        return error_templates.get(error_type, error_templates["general_error"]).strip()
    
    def create_error_buttons(self, username: str = "") -> InlineKeyboardMarkup:
        """Create buttons for error messages"""
        markup = InlineKeyboardMarkup()
        
        if username:
            markup.row(
                InlineKeyboardButton("🔄 Try Again", callback_data=f"github_retry_{username}"),
                InlineKeyboardButton("❌ Cancel", callback_data="github_cancel")
            )
        else:
            markup.row(
                InlineKeyboardButton("📚 View Help", callback_data="github_help")
            )
        
        return markup

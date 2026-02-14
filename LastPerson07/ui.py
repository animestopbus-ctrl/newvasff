from typing import Dict, Tuple, TypedDict
from datetime import datetime
from dataclasses import dataclass

# Type definitions for better type safety
class ButtonConfig(TypedDict, total=False):
    text: str
    url: str
    callback_data: str
    style: str
    icon_custom_emoji_id: str

@dataclass
class ProfileData:
    """Dataclass for GitHub profile data"""
    name: str
    login: str
    id: int
    avatar_url: str
    html_url: str
    blog: str
    location: str
    company: str
    email: str
    hireable: str
    twitter: str
    bio: str
    followers: int
    following: int
    public_repos: int
    public_gists: int
    created_at: str
    updated_at: str

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
        
        # Premium emoji ID for buttons
        self.EMOJI_ID: str = "5474667187258006816"
    
    def format_date(self, date_str: str) -> str:
        """Format ISO date to readable format using pattern matching"""
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
        """Create formatted profile message with Python 3.12 features"""
        # Use walrus operator for cleaner data extraction
        profile_data: ProfileData = ProfileData(
            name=data.get("name") or "N/A",
            login=data.get("login") or "N/A",
            id=data.get("id") or 0,
            avatar_url=data.get("avatar_url") or "",
            html_url=data.get("html_url") or "",
            blog=data.get("blog") or "N/A",
            location=data.get("location") or "N/A",
            company=data.get("company") or "N/A",
            email=data.get("email") or "N/A",
            hireable="✅" if data.get("hireable") else "❌",
            twitter=data.get("twitter_username") or "N/A",
            bio=data.get("bio") or "No bio provided.",
            followers=data.get("followers", 0),
            following=data.get("following", 0),
            public_repos=data.get("public_repos", 0),
            public_gists=data.get("public_gists", 0),
            created_at=self.format_date(data.get("created_at") or "N/A"),
            updated_at=self.format_date(data.get("updated_at") or "N/A"),
        )
        
        # Enhanced f-string with Python 3.12 features
        text: str = f"""
{self.emojis['profile']} <b>GitHub Profile Explorer</b>
        
{self.emojis['name']} <b>{profile_data.name}</b> <i>(@{profile_data.login})</i>

{self.emojis['bio']} <i>"{profile_data.bio}"</i>

📊 <b>GitHub Stats:</b>
{self.emojis['repos']} Repositories: <b>{profile_data.public_repos}</b>
{self.emojis['gists']} Gists: <b>{profile_data.public_gists}</b>
{self.emojis['followers']} Followers: <b>{profile_data.followers}</b> | {self.emojis['following']} Following: <b>{profile_data.following}</b>

👤 <b>Profile Information:</b>
{self.emojis['id']} ID: <code>{profile_data.id}</code>
{self.emojis['location']} Location: {profile_data.location}
{self.emojis['company']} Company: {profile_data.company}
{self.emojis['email']} Email: {profile_data.email}
{self.emojis['hireable']} Hireable: {profile_data.hireable}
{self.emojis['twitter']} Twitter: {profile_data.twitter}
{self.emojis['blog']} Blog: {profile_data.blog}

📅 <b>Account Timeline:</b>
{self.emojis['created']} Created: {profile_data.created_at}
{self.emojis['updated']} Updated: {profile_data.updated_at}

{self.emojis['link']} <a href='{profile_data.html_url}'>View on GitHub</a>
        """.strip()
        
        return profile_data.avatar_url, text
    
    def create_profile_buttons(self, data: Dict) -> Dict[str, list]:
        """Create interactive buttons for GitHub profile using TypedDict"""
        login: str = data.get("login", "")
        html_url: str = data.get("html_url", "")
        repos_url: str = data.get("repos_url", "")
        followers_url: str = data.get("followers_url", "")
        
        buttons: list[list[ButtonConfig]] = [
            [
                ButtonConfig(
                    text="🌟 View Profile",
                    url=html_url,
                    style="primary"
                ),
                ButtonConfig(
                    text="📂 Repositories", 
                    url=repos_url,
                    style="success"
                )
            ],
            [
                ButtonConfig(
                    text="👥 Followers",
                    url=followers_url,
                    style="primary"
                ),
                ButtonConfig(
                    text="🔥 Premium View",
                    callback_data=f"github_premium_{login}",
                    icon_custom_emoji_id=self.EMOJI_ID
                )
            ],
            [
                ButtonConfig(
                    text="🔄 Refresh Data",
                    callback_data=f"github_refresh_{login}",
                    style="secondary"
                )
            ]
        ]
        
        return {"inline_keyboard": buttons}
    
    def create_error_message(self, error_type: str, username: str = "") -> str:
        """Create formatted error messages using match case"""
        error_templates: Dict[str, str] = {
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
    
    def create_error_buttons(self, username: str = "") -> Dict[str, list]:
        """Create buttons for error messages"""
        if username:
            buttons: list[list[ButtonConfig]] = [
                [
                    ButtonConfig(
                        text="🔄 Try Again",
                        callback_data=f"github_retry_{username}",
                        style="primary"
                    ),
                    ButtonConfig(
                        text="❌ Cancel",
                        callback_data="github_cancel",
                        style="danger"
                    )
                ]
            ]
        else:
            buttons: list[list[ButtonConfig]] = [
                [
                    ButtonConfig(
                        text="📚 View Help",
                        callback_data="github_help",
                        style="secondary"
                    )
                ]
            ]
        
        return {"inline_keyboard": buttons}

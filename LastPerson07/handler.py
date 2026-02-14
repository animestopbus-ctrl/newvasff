from .api import fetch_github_data
from .ui import format_profile_text

def register_github_handlers(bot):
    @bot.message_handler(commands=['github'])
    def handle_github(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id, "❌ Please provide a GitHub username.\n\nExample:\n<code>/github rahul</code>", parse_mode="HTML")
            return

        username = parts[1].strip()

        # 1. Get Data from api.py
        data = fetch_github_data(username)

        # 2. Check if api.py returned an error
        if "error" in data:
            bot.send_message(message.chat.id, data["error"], parse_mode="HTML")
            return

        # 3. Get formatted text from ui.py
        text = format_profile_text(data)
        avatar = data.get("avatar_url") or ""

        # 4. Send to user
        try:
            bot.send_photo(message.chat.id, photo=avatar, caption=text, parse_mode="HTML")
        except Exception as e:
            print(f"Send Photo Error: {e}")
            bot.send_message(message.chat.id, "⚠️ Failed to send profile data.")

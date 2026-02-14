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
        avatar = data.get("avatar_url")

        # 4. Send to user (With smart Fallbacks!)
        try:
            if avatar:
                # Try sending photo with caption (Limit: 1024 characters)
                bot.send_photo(message.chat.id, photo=avatar, caption=text, parse_mode="HTML")
            else:
                # If they have no avatar, just send the text
                bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True)
                
        except Exception as e:
            print(f"Caption too long or HTML error: {e}")
            
            try:
                # FALLBACK: Send photo and text separately! (Text Limit: 4096 characters)
                if avatar:
                    bot.send_photo(message.chat.id, photo=avatar)
                bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True)
            except Exception as e2:
                print(f"Complete Send Failure: {e2}")
                bot.send_message(message.chat.id, "⚠️ Failed to format profile data. The user's bio might contain unsupported characters.")

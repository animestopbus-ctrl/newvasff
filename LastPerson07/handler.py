from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .api import fetch_github_data
from .ui import format_profile_text

def register_github_handlers(bot):
    @bot.message_handler(commands=['github'])
    def handle_github(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id, "❌ Please provide a GitHub username.\n\nExample:\n<code>/github LastPerson07</code>", parse_mode="HTML")
            return

        username = parts[1].strip()

        # 1. Get Data
        data = fetch_github_data(username)
        if "error" in data:
            bot.send_message(message.chat.id, data["error"], parse_mode="HTML")
            return

        # 2. Get formatted text and avatar
        text = format_profile_text(data)
        avatar = data.get("avatar_url")
        
        # 3. BUILD THE INLINE KEYBOARD BUTTONS! 🎛️
        markup = InlineKeyboardMarkup()
        html_url = data.get("html_url", f"https://github.com/{username}")
        
        # Create buttons with actual web URLs, not raw API URLs
        btn_profile = InlineKeyboardButton("🔗 Profile", url=html_url)
        btn_repos = InlineKeyboardButton("📁 Repos", url=f"{html_url}?tab=repositories")
        btn_followers = InlineKeyboardButton("👤 Followers", url=f"{html_url}?tab=followers")
        btn_following = InlineKeyboardButton("➡️ Following", url=f"{html_url}?tab=following")
        btn_gists = InlineKeyboardButton("📑 Gists", url=f"https://gist.github.com/{username}")
        
        # Arrange them neatly: 2 on the first row, 2 on the second, 1 on the bottom
        markup.row(btn_profile, btn_repos)
        markup.row(btn_followers, btn_following)
        markup.row(btn_gists)

        # 4. Send to user (Now with reply_markup=markup attached!)
        try:
            if avatar:
                bot.send_photo(message.chat.id, photo=avatar, caption=text, parse_mode="HTML", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)
                
        except Exception as e:
            print(f"Caption too long or HTML error: {e}")
            try:
                # FALLBACK: Send photo and text separately
                if avatar:
                    bot.send_photo(message.chat.id, photo=avatar)
                bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)
            except Exception as e2:
                print(f"Complete Send Failure: {e2}")
                bot.send_message(message.chat.id, "⚠️ Failed to format profile data.")

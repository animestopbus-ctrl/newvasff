import json
import requests
from .api import fetch_github_data
from .ui import format_profile_text

def register_github_handlers(bot):

    # ==========================================
    # 🤖 FEATURE 1: DYNAMIC PROFILE PIC (API 9.4)
    # ==========================================
    @bot.message_handler(commands=['setavatar'])
    def handle_set_avatar(message):
        bot.send_message(message.chat.id, "🖼️ <b>To change my profile picture:</b>\nSend me a photo, and put <code>/setavatar</code> in the caption!", parse_mode="HTML")

    @bot.message_handler(content_types=['photo'])
    def save_and_set_avatar(message):
        if message.caption and '/setavatar' in message.caption:
            bot.send_message(message.chat.id, "🔄 Uploading new face to Telegram...")
            try:
                # 1. Download the photo you sent
                file_info = bot.get_file(message.photo[-1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                
                # 2. Save it temporarily
                with open("temp_avatar.png", 'wb') as new_file:
                    new_file.write(downloaded_file)
                
                # 3. RAW API REQUEST TO TELEGRAM (Bypassing the library!)
                url = f"https://api.telegram.org/bot{bot.token}/setMyProfilePhoto"
                with open("temp_avatar.png", "rb") as photo:
                    res = requests.post(url, files={"photo": photo}).json()
                
                if res.get("ok"):
                    bot.reply_to(message, "✅ BOOM! My profile picture has been updated.")
                else:
                    bot.reply_to(message, f"❌ Telegram rejected it: {res.get('description')}")
            except Exception as e:
                bot.reply_to(message, f"⚠️ Error changing avatar: {e}")

    # ==========================================
    # 🎨 FEATURE 2: COLORED BUTTONS (API 9.4)
    # ==========================================
    @bot.message_handler(commands=['github'])
    def handle_github(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id, "❌ Please provide a GitHub username.\n\nExample:\n<code>/github LastPerson07</code>", parse_mode="HTML")
            return

        username = parts[1].strip()
        data = fetch_github_data(username)

        if "error" in data:
            bot.send_message(message.chat.id, data["error"], parse_mode="HTML")
            return

        text = format_profile_text(data)
        avatar = data.get("avatar_url")
        html_url = data.get("html_url", f"https://github.com/{username}")
        
        # 🎛️ THE RAW JSON KEYBOARD (Forces Telegram 9.4 Features)
        # Note: If you have a Premium emoji ID, replace "emoji_id" with the string of numbers!
        raw_markup = {
            "inline_keyboard": [
                [
                    # Primary color button!
                    {"text": "🔗 Profile", "url": html_url, "color": "primary"}
                ],
                [
                    # Default colors for standard links
                    {"text": "📁 Repos", "url": f"{html_url}?tab=repositories"},
                    {"text": "👤 Followers", "url": f"{html_url}?tab=followers"}
                ],
                [
                    # Secondary color!
                    {"text": "➡️ Following", "url": f"{html_url}?tab=following", "color": "secondary"},
                    {"text": "📑 Gists", "url": f"https://gist.github.com/{username}"}
                ]
            ]
        }
        
        # Convert dictionary to JSON string so Telegram can read it
        markup_json = json.dumps(raw_markup)

        try:
            if avatar:
                bot.send_photo(message.chat.id, photo=avatar, caption=text, parse_mode="HTML", reply_markup=markup_json)
            else:
                bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup_json)
                
        except Exception as e:
            print(f"Send error: {e}")
            try:
                if avatar:
                    bot.send_photo(message.chat.id, photo=avatar)
                bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup_json)
            except Exception as e2:
                bot.send_message(message.chat.id, "⚠️ Failed to format profile data.")

#!/usr/bin/env python3.12
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add package to path using pathlib
package_path = Path(__file__).parent / "LastPerson07"
sys.path.insert(0, str(package_path))

from telebot import TeleBot
from LastPerson07.start import setup_LastPerson07_handlers

# Bot configuration using walrus operator
if not (BOT_TOKEN := os.getenv('BOT_TOKEN')):
    print("❌ Please set BOT_TOKEN environment variable")
    sys.exit(1)

# Initialize bot with type hint
bot: TeleBot = TeleBot(BOT_TOKEN)

# Setup handlers
setup_LastPerson07_handlers(bot)

# Enhanced welcome message with match case pattern
@bot.message_handler(commands=['start'])
def send_welcome(message) -> None:
    welcome_text = """
🌟 <b>Welcome to LastPerson07 GitHub Explorer!</b>

I can fetch detailed GitHub profile information with beautiful interactive buttons.

🔍 <b>How to use:</b>
Send <code>/github username</code> to explore any GitHub profile!

✨ <b>New Premium Features:</b>
• Colored button UI (primary, success, danger, secondary)
• Custom emoji integration
• Interactive action buttons
• Real-time data refresh

💡 <b>Example:</b>
<code>/github torvalds</code>

Type /help for more commands.
    """.strip()
    
    # Premium buttons with emoji ID
    EMOJI_ID: str = "5474667187258006816"
    
    welcome_buttons: dict[str, list] = {
        "inline_keyboard": [
            [
                {
                    "text": "🚀 Get Started",
                    "callback_data": "github_retry_torvalds",
                    "style": "primary"
                },
                {
                    "text": "📚 View Help", 
                    "callback_data": "github_help",
                    "style": "secondary"
                }
            ],
            [
                {
                    "text": "🔥 Premium Demo",
                    "callback_data": "github_premium_demo",
                    "icon_custom_emoji_id": EMOJI_ID
                }
            ]
        ]
    }
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=welcome_buttons)

# Handle non-command messages with structural pattern matching
@bot.message_handler(func=lambda message: True)
def handle_non_command(message) -> None:
    help_text = """
🤖 <b>LastPerson07 GitHub Bot</b>

I'm here to help you explore GitHub profiles with premium button UI!

Use <code>/github username</code> to get started.

🔍 <b>Try it now:</b>
    """.strip()
    
    buttons: dict[str, list] = {
        "inline_keyboard": [
            [
                {
                    "text": "🔍 Search Profile",
                    "switch_inline_query_current_chat": "/github "
                }
            ],
            [
                {
                    "text": "🌰 Example: torvalds",
                    "callback_data": "github_retry_torvalds",
                    "style": "secondary"
                },
                {
                    "text": "⭐ Premium",
                    "callback_data": "github_premium_demo",
                    "icon_custom_emoji_id": "5474667187258006816"
                }
            ]
        ]
    }
    
    bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=buttons)

if __name__ == "__main__":
    print("🤖 LastPerson07 GitHub Bot is running on Python 3.12.9...")
    bot.polling(none_stop=True)

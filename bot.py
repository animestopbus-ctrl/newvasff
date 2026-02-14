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
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from LastPerson07.start import setup_LastPerson07_handlers

# Bot configuration using walrus operator
if not (BOT_TOKEN := os.getenv('BOT_TOKEN')):
    print("❌ Please set BOT_TOKEN environment variable")
    sys.exit(1)

# Initialize bot with type hint
bot: TeleBot = TeleBot(BOT_TOKEN)

# Setup handlers
setup_LastPerson07_handlers(bot)

# Enhanced welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message) -> None:
    welcome_text = """
🌟 <b>Welcome to LastPerson07 GitHub Explorer!</b>

I can fetch detailed GitHub profile information with interactive buttons.

🔍 <b>How to use:</b>
Send <code>/github username</code> to explore any GitHub profile!

✨ <b>Features:</b>
• Beautiful UI with interactive buttons
• GitHub profile exploration
• Quick action buttons
• Real-time data refresh

💡 <b>Example:</b>
<code>/github torvalds</code>

Type /help for more commands.
    """.strip()
    
    # Create welcome buttons using compatible method
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🚀 Get Started", callback_data="github_retry_torvalds"),
        InlineKeyboardButton("📚 View Help", callback_data="github_help")
    )
    markup.row(
        InlineKeyboardButton("⭐ Premium Demo", callback_data="github_premium_demo")
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=markup)

# Handle non-command messages
@bot.message_handler(func=lambda message: True)
def handle_non_command(message) -> None:
    help_text = """
🤖 <b>LastPerson07 GitHub Bot</b>

I'm here to help you explore GitHub profiles!

Use <code>/github username</code> to get started.

🔍 <b>Try it now:</b>
    """.strip()
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔍 Search Profile", switch_inline_query_current_chat="/github ")
    )
    markup.row(
        InlineKeyboardButton("🌰 Example: torvalds", callback_data="github_retry_torvalds"),
        InlineKeyboardButton("⭐ Premium", callback_data="github_premium_demo")
    )
    
    bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    print("🤖 LastPerson07 GitHub Bot is running on Python 3.12.9...")
    bot.polling(none_stop=True)

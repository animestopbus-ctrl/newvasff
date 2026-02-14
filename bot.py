#!/usr/bin/env python3.12
import os
import sys
import time
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
    
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    
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
    
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔍 Search Profile", switch_inline_query_current_chat="/github ")
    )
    markup.row(
        InlineKeyboardButton("🌰 Example: torvalds", callback_data="github_retry_torvalds"),
        InlineKeyboardButton("⭐ Premium", callback_data="github_premium_demo")
    )
    
    bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=markup)

def safe_polling(retry_count: int = 0) -> None:
    """Safe polling with retry logic for conflict errors"""
    max_retries = 5
    base_delay = 10  # seconds
    
    try:
        print(f"🤖 Starting LastPerson07 GitHub Bot (Attempt {retry_count + 1})...")
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        error_msg = str(e).lower()
        
        # Check for conflict error (multiple instances)
        if "conflict" in error_msg and "getupdates" in error_msg:
            if retry_count < max_retries:
                delay = base_delay * (2 ** retry_count)  # Exponential backoff
                print(f"⚠️  Bot conflict detected. Retrying in {delay} seconds...")
                time.sleep(delay)
                safe_polling(retry_count + 1)
            else:
                print("❌ Max retries exceeded. Another bot instance might be running.")
                print("💡 Solution: Check if multiple containers/processes are running your bot.")
        else:
            print(f"❌ Unexpected error: {e}")
            # Restart after a delay for other errors
            if retry_count < max_retries:
                delay = 30
                print(f"🔄 Restarting in {delay} seconds...")
                time.sleep(delay)
                safe_polling(retry_count + 1)

if __name__ == "__main__":
    safe_polling()

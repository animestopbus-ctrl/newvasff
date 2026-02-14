from __future__ import annotations
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from .handler import LastPerson07Handler

def setup_LastPerson07_handlers(bot):
    """Setup LastPerson07 command handlers"""
    handler: LastPerson07Handler = LastPerson07Handler()
    
    @bot.message_handler(commands=['github'])
    def github_command(message):
        params = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else ""
        
        # Store message in bot object for handler access
        bot.message = message
        handler.handle_github_command(bot, params)
    
    # Add callback query handler
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        handler.handle_callback_query(bot, call)
    
    # Add help command
    @bot.message_handler(commands=['help'])
    def help_command(message):
        help_text = """
🤖 <b>LastPerson07 GitHub Bot</b>

<b>Available Commands:</b>
• <code>/github username</code> - Get GitHub profile info with interactive buttons
• <code>/help</code> - Show this help message

✨ <b>Features:</b>
• Beautiful UI with interactive buttons
• GitHub profile exploration
• Quick action buttons
• Real-time data refresh

💡 <b>Examples:</b>
<code>/github torvalds</code>
<code>/github gaearon</code>
<code>/github vostok</code>

🔍 Get detailed GitHub profile information instantly!
        """.strip()
        
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("🚀 Try Example", callback_data="github_retry_torvalds"),
            InlineKeyboardButton("⭐ Premium Demo", callback_data="github_premium_demo")
        )
        
        bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=markup)

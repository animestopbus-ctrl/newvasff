from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telebot import TeleBot

from .handler import LastPerson07Handler

def setup_LastPerson07_handlers(bot: TeleBot) -> None:
    """Setup LastPerson07 command handlers with Python 3.12 features"""
    handler: LastPerson07Handler = LastPerson07Handler(bot)
    
    @bot.message_handler(commands=['github'])
    def github_command(message) -> None:
        handler.handle_github_command(message)
    
    # Add callback query handler
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call) -> None:
        handler.handle_callback_query(call)
    
    # Add help command with premium buttons
    @bot.message_handler(commands=['help'])
    def help_command(message) -> None:
        help_text: str = """
🤖 <b>LastPerson07 GitHub Bot</b>

<b>Available Commands:</b>
• <code>/github username</code> - Get GitHub profile info with interactive buttons
• <code>/help</code> - Show this help message

✨ <b>Premium Features:</b>
• Beautiful UI with colored buttons
• Interactive profile exploration
• Quick action buttons
• Real-time data refresh

💡 <b>Examples:</b>
<code>/github torvalds</code>
<code>/github gaearon</code>
<code>/github vostok</code>

🔍 Get detailed GitHub profile information instantly!
        """.strip()
        
        buttons: dict[str, list] = {
            "inline_keyboard": [
                [
                    {
                        "text": "🚀 Try Example",
                        "callback_data": "github_retry_torvalds",
                        "style": "primary"
                    },
                    {
                        "text": "⭐ Premium Demo",
                        "callback_data": "github_premium_demo",
                        "icon_custom_emoji_id": "5474667187258006816"
                    }
                ]
            ]
        }
        
        bot.send_message(message.chat.id, help_text, parse_mode="HTML", reply_markup=buttons)

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telebot import TeleBot
    from telebot.types import Message, CallbackQuery

from .api import LastPerson07API
from .ui import LastPerson07UI

class LastPerson07Handler:
    def __init__(self, bot: TeleBot) -> None:
        self.bot: TeleBot = bot
        self.api: LastPerson07API = LastPerson07API()
        self.ui: LastPerson07UI = LastPerson07UI()
    
    def handle_github_command(self, message: Message) -> None:
        """Main handler for /github command with Python 3.12 features"""
        # Extract params using walrus operator
        if not (params := getattr(message, 'text', '').split(maxsplit=1)[1:]):
            error_msg: str = self.ui.create_error_message("no_params")
            error_buttons: dict = self.ui.create_error_buttons()
            self.bot.send_message(message.chat.id, error_msg, parse_mode="HTML", reply_markup=error_buttons)
            return
        
        username: str = params[0].strip()
        
        # Validate username format
        is_valid, validation_msg = self.api.validate_username(username)
        if not is_valid:
            error_msg = self.ui.create_error_message("invalid_username", username)
            error_buttons = self.ui.create_error_buttons(username)
            self.bot.send_message(message.chat.id, error_msg, parse_mode="HTML", reply_markup=error_buttons)
            return
        
        # Show typing action
        self.bot.send_chat_action(message.chat.id, 'typing')
        
        # Fetch GitHub data
        data, error = self.api.fetch_user_data(username)
        
        # Enhanced error handling with pattern matching
        if error:
            match error.lower():
                case err if "not found" in err:
                    error_msg = self.ui.create_error_message("user_not_found", username)
                case err if "rate limit" in err:
                    error_msg = self.ui.create_error_message("rate_limit")
                case err if "timeout" in err:
                    error_msg = self.ui.create_error_message("timeout")
                case _:
                    error_msg = self.ui.create_error_message("general_error")
            
            error_buttons = self.ui.create_error_buttons(username)
            self.bot.send_message(message.chat.id, error_msg, parse_mode="HTML", reply_markup=error_buttons)
            return
        
        # Create and send formatted response with buttons
        avatar_url, formatted_text = self.ui.create_profile_message(data)
        buttons = self.ui.create_profile_buttons(data)
        
        if avatar_url and avatar_url != "N/A":
            self.bot.send_photo(
                message.chat.id,
                photo=avatar_url,
                caption=formatted_text,
                parse_mode="HTML",
                reply_markup=buttons
            )
        else:
            # Fallback to text message if no avatar
            self.bot.send_message(
                message.chat.id,
                formatted_text,
                parse_mode="HTML",
                reply_markup=buttons
            )
    
    def handle_callback_query(self, call: CallbackQuery) -> None:
        """Handle button callbacks with pattern matching"""
        try:
            # Use Python 3.12 pattern matching for callback data
            match call.data:
                case data if data.startswith("github_retry_"):
                    username: str = data.removeprefix("github_retry_")
                    self.bot.answer_callback_query(call.id, f"🔄 Retrying for {username}...")
                    # Create a mock message object for the handler
                    message = type('MockMessage', (), {
                        'chat': type('Chat', (), {'id': call.message.chat.id}),
                        'text': f'/github {username}'
                    })()
                    self.handle_github_command(message)
                    
                case data if data.startswith("github_refresh_"):
                    username = data.removeprefix("github_refresh_")
                    self.bot.answer_callback_query(call.id, f"🔄 Refreshing {username}...")
                    message = type('MockMessage', (), {
                        'chat': type('Chat', (), {'id': call.message.chat.id}),
                        'text': f'/github {username}'
                    })()
                    self.handle_github_command(message)
                    
                case "github_help":
                    self.bot.answer_callback_query(call.id, "📚 Showing help...")
                    self.bot.send_message(
                        call.message.chat.id,
                        "🤖 <b>GitHub Bot Help</b>\n\nUse <code>/github username</code> to explore GitHub profiles!",
                        parse_mode="HTML"
                    )
                    
                case "github_cancel":
                    self.bot.answer_callback_query(call.id, "❌ Cancelled")
                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text="❌ Operation cancelled."
                    )
                    
                case _:
                    self.bot.answer_callback_query(call.id, "❓ Unknown command")
                    
        except Exception as e:
            self.bot.answer_callback_query(call.id, "⚠️ Error processing request")
  
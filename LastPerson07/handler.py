from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telebot import TeleBot
    from telebot.types import Message, CallbackQuery

from .api import LastPerson07API
from .ui import LastPerson07UI

class LastPerson07Handler:
    def __init__(self) -> None:
        self.api: LastPerson07API = LastPerson07API()
        self.ui: LastPerson07UI = LastPerson07UI()
    
    def handle_github_command(self, bot: TeleBot, params: str) -> None:
        """Main handler for /github command"""
        # Check if params are provided
        if not params:
            error_msg: str = self.ui.create_error_message("no_params")
            error_buttons = self.ui.create_error_buttons()
            bot.send_message(bot.message.chat.id, error_msg, parse_mode="HTML", reply_markup=error_buttons)
            return
        
        username: str = params.strip()
        
        # Validate username format
        is_valid, validation_msg = self.api.validate_username(username)
        if not is_valid:
            error_msg = self.ui.create_error_message("invalid_username", username)
            error_buttons = self.ui.create_error_buttons(username)
            bot.send_message(bot.message.chat.id, error_msg, parse_mode="HTML", reply_markup=error_buttons)
            return
        
        # Show typing action
        bot.send_chat_action(bot.message.chat.id, 'typing')
        
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
            bot.send_message(bot.message.chat.id, error_msg, parse_mode="HTML", reply_markup=error_buttons)
            return
        
        # Create and send formatted response with buttons
        avatar_url, formatted_text = self.ui.create_profile_message(data)
        buttons = self.ui.create_profile_buttons(data)
        
        if avatar_url and avatar_url != "N/A":
            bot.send_photo(
                bot.message.chat.id,
                photo=avatar_url,
                caption=formatted_text,
                parse_mode="HTML",
                reply_markup=buttons
            )
        else:
            # Fallback to text message if no avatar
            bot.send_message(
                bot.message.chat.id,
                formatted_text,
                parse_mode="HTML",
                reply_markup=buttons
            )
    
    def handle_callback_query(self, bot: TeleBot, call: CallbackQuery) -> None:
        """Handle button callbacks"""
        try:
            # Use Python 3.12 pattern matching for callback data
            match call.data:
                case data if data.startswith("github_retry_"):
                    username: str = data.removeprefix("github_retry_")
                    bot.answer_callback_query(call.id, f"🔄 Retrying for {username}...")
                    # For callback queries, we need to send a new message
                    bot.send_message(call.message.chat.id, f"🔄 Fetching GitHub profile for {username}...")
                    self.handle_github_command(bot, username)
                    
                case data if data.startswith("github_refresh_"):
                    username = data.removeprefix("github_refresh_")
                    bot.answer_callback_query(call.id, f"🔄 Refreshing {username}...")
                    bot.send_message(call.message.chat.id, f"🔄 Refreshing GitHub profile for {username}...")
                    self.handle_github_command(bot, username)
                    
                case "github_help":
                    bot.answer_callback_query(call.id, "📚 Showing help...")
                    bot.send_message(
                        call.message.chat.id,
                        "🤖 <b>GitHub Bot Help</b>\n\nUse <code>/github username</code> to explore GitHub profiles!",
                        parse_mode="HTML"
                    )
                    
                case "github_cancel":
                    bot.answer_callback_query(call.id, "❌ Cancelled")
                    bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text="❌ Operation cancelled.",
                        parse_mode="HTML"
                    )
                    
                case _:
                    bot.answer_callback_query(call.id, "❓ Unknown command")
                    
        except Exception as e:
            bot.answer_callback_query(call.id, "⚠️ Error processing request")

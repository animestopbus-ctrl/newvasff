def register_start_handlers(bot):
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        welcome_text = (
            "👋 Welcome! I am a GitHub lookup bot.\n\n"
            "Usage: <code>/github username</code>"
        )
        bot.reply_to(message, welcome_text, parse_mode="HTML")

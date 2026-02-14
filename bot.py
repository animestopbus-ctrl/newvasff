import telebot
import os
from flask import Flask, request

from LastPerson07.start import register_start_handlers
from LastPerson07.handler import register_github_handlers

# Fetch environment variables from Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Register the commands from your LastPerson07 package
register_start_handlers(bot)
register_github_handlers(bot)

# 1. The Webhook Route (Listens for Telegram's messages)
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

# 2. A simple Health Check Route (So Render knows your app is alive)
@app.route('/')
def index():
    return "Bot is running on Render!", 200

if __name__ == "__main__":
    # This is only for local testing. In production, Gunicorn takes over.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

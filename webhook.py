#!/usr/bin/env python3.12
import os
import sys
from pathlib import Path
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

package_path = Path(__file__).parent / "LastPerson07"
sys.path.insert(0, str(package_path))

from telebot import TeleBot
from LastPerson07.start import setup_LastPerson07_handlers

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ Please set BOT_TOKEN environment variable")
    sys.exit(1)

bot = TeleBot(BOT_TOKEN)
setup_LastPerson07_handlers(bot)

app = Flask(__name__)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Set this in your environment

@app.route('/')
def index():
    return "🤖 LastPerson07 GitHub Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 400

if __name__ == '__main__':
    if WEBHOOK_URL:
        # Set webhook for production
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        print("🌐 Webhook mode activated")
    else:
        # Fallback to polling for development
        print("🔍 Polling mode activated")
        bot.polling(none_stop=True)

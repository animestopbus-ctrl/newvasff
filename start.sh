#!/bin/bash

# 1. Tell Telegram to send messages to your Render URL
python -c "import telebot, os; bot = telebot.TeleBot(os.environ.get('BOT_TOKEN')); bot.remove_webhook(); bot.set_webhook(url=os.environ.get('WEBHOOK_URL') + '/' + os.environ.get('BOT_TOKEN'))"

# 2. Start the Flask application using Gunicorn on Render's assigned port
gunicorn bot:app --bind 0.0.0.0:$PORT

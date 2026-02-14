import telebot
import os
from flask import Flask, request

from LastPerson07.start import register_start_handlers
from LastPerson07.handler import register_github_handlers

# Fetch environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") # e.g., https://newvasff.onrender.com

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Register your commands
register_start_handlers(bot)
register_github_handlers(bot)

# 1. Health check route
@app.route('/')
def index():
    return "🚀 Bot is running perfectly on Render!", 200

# 2. The Webhook Route (Where Telegram sends messages)
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Forbidden', 403

# 3. THE MAGIC LINK - Run this once to connect Telegram!
@app.route('/set_webhook')
def set_webhook():
    if not WEBHOOK_URL:
        return "❌ Error: WEBHOOK_URL is missing in Render Environment Variables.", 400
    
    # Remove old webhook and set the new one
    bot.remove_webhook()
    success = bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    
    if success:
        return f"✅ SUCCESS! Webhook is now connected to: {WEBHOOK_URL}", 200
    else:
        return "❌ FAILED to set webhook.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

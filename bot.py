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
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ByPass | GitHub AI Bot</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            :root {
                --bg: #030712;
                --primary: #3b82f6;
                --glass: rgba(255, 255, 255, 0.03);
                --border: rgba(255, 255, 255, 0.1);
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, sans-serif;
                background: radial-gradient(circle at top right, #1e3a8a, var(--bg));
                color: #f3f4f6;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            /* Floating Background Circles for Depth */
            .blob {
                position: absolute;
                width: 300px;
                height: 300px;
                background: var(--primary);
                filter: blur(80px);
                border-radius: 50%;
                opacity: 0.15;
                z-index: -1;
                animation: float 10s infinite alternate;
            }
            @keyframes float { from { transform: translate(-20%, -20%); } to { transform: translate(20%, 20%); } }

            /* Modern Glass Card */
            .dashboard {
                background: var(--glass);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 40px;
                max-width: 480px;
                width: 90%;
                text-align: center;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                transition: transform 0.3s ease;
            }
            .dashboard:hover { transform: translateY(-5px); }

            .status-badge {
                display: inline-flex;
                align-items: center;
                background: rgba(16, 185, 129, 0.1);
                color: #10b981;
                padding: 6px 16px;
                border-radius: 50px;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 24px;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            .status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 8px; animation: pulse 2s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

            h1 { font-size: 32px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.5px; }
            p { color: #9ca3af; line-height: 1.6; margin-bottom: 32px; font-size: 16px; }

            /* Modern Button Design */
            .btn {
                display: flex;
                align-items: center;
                justify-content: center;
                background: #ffffff;
                color: #000000;
                text-decoration: none;
                padding: 16px 32px;
                border-radius: 14px;
                font-weight: 700;
                font-size: 16px;
                gap: 10px;
                transition: all 0.2s ease;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }
            .btn:hover { background: #e5e7eb; transform: scale(1.02); }
            
            .features {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-top: 30px;
                text-align: left;
            }
            .feature-item {
                font-size: 12px;
                color: #6b7280;
                display: flex;
                align-items: center;
                gap: 8px;
            }
        </style>
    </head>
    <body>
        <div class="blob"></div>
        <div class="dashboard">
            <div class="status-badge">
                <span class="status-dot"></span> API v9.4 Connected
            </div>
            <h1>ByPass Bot</h1>
            <p>The next-generation GitHub explorer for Telegram. Fast, secure, and styled for the future.</p>
            
            <a href="https://t.me/YOUR_BOT_USERNAME" class="btn">
                <i class="fab fa-telegram"></i> Launch in Telegram
            </a>

            <div class="features">
                <div class="feature-item"><i class="fas fa-check-circle" style="color:var(--primary)"></i> 24/7 Uptime</div>
                <div class="feature-item"><i class="fas fa-check-circle" style="color:var(--primary)"></i> VIP API Access</div>
                <div class="feature-item"><i class="fas fa-check-circle" style="color:var(--primary)"></i> UI 9.4 Support</div>
                <div class="feature-item"><i class="fas fa-check-circle" style="color:var(--primary)"></i> Analytics Ready</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content, 200

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


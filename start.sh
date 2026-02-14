#!/bin/bash

echo "🚀 Starting LastPerson07 GitHub Bot (Python 3.12.9)..."

# Check Python version
PYTHON_VERSION=$(python3.12 --version 2>/dev/null | cut -d' ' -f2)
if [ "$PYTHON_VERSION" != "3.12.9" ]; then
    echo "❌ Error: Python 3.12.9 is required. Found: $PYTHON_VERSION"
    echo "💡 Install with: pyenv install 3.12.9"
    exit 1
fi

# Check if BOT_TOKEN is set using parameter expansion
if [[ -z "${BOT_TOKEN}" ]]; then
    echo "❌ Error: BOT_TOKEN environment variable is not set."
    echo "💡 Please set it with: export BOT_TOKEN='your_bot_token_here'"
    exit 1
fi

# Install requirements using Python 3.12
echo "📦 Installing requirements with Python 3.12.9..."
python3.12 -m pip install -r requirements.txt

# Run the bot
echo "🤖 Bot is starting with Python 3.12.9..."
python3.12 bot.py

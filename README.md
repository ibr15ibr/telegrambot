# Prayer Telegram Bot

A Telegram bot that sends random Islamic prayers and supplications.

## Features
- `/start` - Start the bot and get welcome message
- `/random` - Get a random prayer from the collection

## Local Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the bot:
```bash
python bot.py
```

## Hosting Options

### 1. PythonAnywhere (Recommended for Beginners)
1. Create an account at [PythonAnywhere](https://www.pythonanywhere.com)
2. Go to Files tab and upload all your files
3. Open a Bash console and create a virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.9 mybot
pip install -r requirements.txt
```
4. Go to Tasks tab and add a new task:
```bash
python /home/yourusername/bot.py
```

### 2. Heroku
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login and create a new app:
```bash
heroku login
heroku create your-bot-name
```
3. Set your bot token:
```bash
heroku config:set BOT_TOKEN=your_bot_token
```
4. Deploy:
```bash
git push heroku main
```

### 3. Railway.app
1. Create an account at [Railway](https://railway.app)
2. Connect your GitHub repository
3. Create a new project from GitHub
4. Add environment variable BOT_TOKEN
5. Deploy

## Environment Variables
- `BOT_TOKEN` - Your Telegram bot token (optional, falls back to hardcoded token)

## Files
- `bot.py` - Main bot code
- `txt` - Collection of prayers
- `requirements.txt` - Python dependencies
- `Procfile` - For Heroku/Railway deployment

## Logging
The bot includes logging to help track usage and errors. Logs include:
- Bot start/stop events
- User interactions
- Errors and warnings

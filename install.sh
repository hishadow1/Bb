#!/bin/bash

# Clone repo if not already
if [ ! -d "vps-discord-bot" ]; then
  git clone https://github.com/hishadow1/Bb.git
fi

cd vps-discord-bot

# Install Python if not found
if ! command -v python3 &>/dev/null; then
  apt update && apt install -y python3 python3-pip
fi

# Install dependencies
pip3 install -U discord.py

# Ask for bot token
if [ ! -f "token.txt" ]; then
  echo "Enter your Discord Bot Token:"
  read token
  echo "$token" > token.txt
fi

# Replace token in bot.py automatically
sed -i "s|bot.run(\"YOUR_BOT_TOKEN\")|bot.run(open('token.txt').read().strip())|" bot.py

# Run with nohup (24/7)
nohup python3 bot.py > log.txt 2>&1 &
echo "✅ Bot started with nohup. Log: log.txt"

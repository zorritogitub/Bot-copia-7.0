#!/bin/bash
mkdir -p /tmp/bot-health-empty
python3 -m http.server "${PORT:-10000}" --bind 0.0.0.0 --directory /tmp/bot-health-empty &
exec python3 bot.py

#!/bin/bash
python3 -m http.server "${PORT:-10000}" --bind 0.0.0.0 --directory /tmp &
exec python3 bot.py

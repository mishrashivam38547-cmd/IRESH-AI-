# IRESH AI v2 — Termux Voice Assistant

## Update an existing installation
In Termux, from the extracted project folder:
```bash
bash install_1.sh
source ~/.bashrc
iresh
```
Or run directly:
```bash
python iresh.py
```

## Features
- Speech input using `termux-speech-to-text`
- Spoken replies using `termux-tts-speak` when available
- Allow-listed app launching: WhatsApp, YouTube, Chrome, Settings, Gmail, Instagram, Telegram, Maps, Play Store
- WhatsApp message draft: enters phone number and message, then opens `wa.me` after explicit `OPEN` confirmation
- Experimental wake-word loop: press `w`, then say “Hey Iresh” and a command

## WhatsApp safety/limitation
This version does **not** auto-press Send. It opens a WhatsApp chat with a prefilled message; verify recipient and message and tap Send yourself. This prevents accidental messages and works without hidden UI automation.

## Wake word limitations
This is not a native always-on hotword engine. It repeatedly invokes Android speech recognition, may require internet, may use battery, and may not work while Termux is backgrounded. Press Ctrl+C to stop wake mode.

## Requirements
- Termux and Termux:API Android app installed from the same trusted source
- `pkg install python termux-api`
- Android microphone permission for Termux:API

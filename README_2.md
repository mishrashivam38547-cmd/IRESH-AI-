# IRESH AI — Termux Voice Assistant

A beginner-friendly Hindi/English voice assistant for Android Termux.

## Features
- Voice input via `termux-speech-to-text` (requires the separate Android Termux:API app and Android microphone permission)
- Spoken responses via `termux-tts-speak`, if available
- Opens WhatsApp, YouTube, Chrome, and Google
- Google web search
- SMS compose/send flow with explicit `SEND` confirmation
- Safe allow-listed commands; it does **not** execute arbitrary shell commands from speech

## Install from GitHub in Termux

1. Install Termux and Termux:API from the same trusted source (for example, the official F-Droid listings or the Termux GitHub releases). Avoid mixing installation sources.
2. In Termux, run:

```bash
pkg update
pkg install git
git clone https://github.com/YOUR_GITHUB_USERNAME/iresh-ai.git
cd iresh-ai
bash install.sh
source ~/.bashrc
iresh
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username and repository name if different.

## Install from a downloaded ZIP

Extract the ZIP in Termux, `cd` into the extracted folder, then run:

```bash
bash install.sh
source ~/.bashrc
iresh
```

## Commands
- Say or type `WhatsApp kholo`
- Say or type `YouTube kholo`
- Say or type `Chrome kholo`
- Say or type `Google kholo`
- Say or type `search Free Fire tips`
- Say or type `time batao`
- Say or type `SMS bhejo`
- Say or type `help`
- Say or type `band ho jao`

Press Enter at the prompt to use voice recognition. Type a command to use text mode. Press `q` to quit.

## Important limitations
- Android may require you to grant microphone, SMS, and notification permissions.
- Voice recognition language/options depend on the Android speech recognizer installed on your phone. Internet may be needed.
- The SMS feature sends only after you type `SEND`; mobile charges may apply.
- This starter version does not directly automate WhatsApp message sending or arbitrary in-app taps. Android restricts cross-app control; those features need an explicitly enabled Accessibility-based Android service and should use confirmation before sending.
- Some package names vary by phone/manufacturer.

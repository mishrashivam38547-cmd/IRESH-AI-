#!/usr/bin/env python3
"""IRESH AI — Termux voice assistant (starter release).

Voice input is triggered by typing a command or using the microphone via Termux:API.
Speech recognition uses Android's available speech recognizer through termux-speech-to-text.
"""
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse

APP_NAME = "IRESH AI"
VERSION = "1.0.0"

def run(args, capture=False, timeout=20):
    try:
        return subprocess.run(args, text=True, capture_output=capture, timeout=timeout, check=False)
    except FileNotFoundError:
        print(f"[!] Command not found: {args[0]}")
    except subprocess.TimeoutExpired:
        print("[!] Command timed out.")
    return None

def speak(text):
    print(f"\n{APP_NAME}: {text}")
    if shutil.which("termux-tts-speak"):
        run(["termux-tts-speak", text], timeout=30)

def listen():
    if not shutil.which("termux-speech-to-text"):
        speak("Speech tool missing. Install Termux API app and package.")
        return ""
    print("\n🎙️ Listening... बोलिए.")
    result = run(["termux-speech-to-text"], capture=True, timeout=60)
    if not result:
        return ""
    text = (result.stdout or "").strip()
    if text:
        print(f"You: {text}")
    else:
        print("[!] कोई आवाज़/टेक्स्ट नहीं मिला।")
    return text

def open_app(package, label):
    if not shutil.which("monkey"):
        speak("Android app launcher command is unavailable.")
        return
    result = run(["monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"], capture=True)
    if result and result.returncode == 0:
        speak(f"{label} खोल रहा हूँ।")
    else:
        speak(f"{label} नहीं खुल पाया। ऐप इंस्टॉल है या नहीं जाँचें।")

def open_url(url, label):
    if shutil.which("termux-open-url"):
        run(["termux-open-url", url])
        speak(f"{label} खोल रहा हूँ।")
    else:
        speak("termux-open-url उपलब्ध नहीं है।")

def send_sms_flow():
    speak("SMS भेजने के लिए नंबर और संदेश टर्मिनल में दर्ज करें। भेजने से पहले पुष्टि होगी।")
    number = input("मोबाइल नंबर (country code सहित बेहतर): ").strip()
    if not re.fullmatch(r"\+?[0-9]{7,15}", number):
        speak("नंबर सही नहीं लग रहा। रद्द किया।")
        return
    message = input("SMS संदेश: ").strip()
    if not message:
        speak("खाली संदेश नहीं भेजा।")
        return
    print(f"\nनंबर: {number}\nसंदेश: {message}")
    confirm = input("SMS भेजने के लिए SEND लिखें: ").strip()
    if confirm != "SEND":
        speak("रद्द कर दिया।")
        return
    if not shutil.which("termux-sms-send"):
        speak("termux-sms-send नहीं मिला। Termux:API ऐप और पैकेज इंस्टॉल करें।")
        return
    result = run(["termux-sms-send", "-n", number, message], timeout=30)
    if result and result.returncode == 0:
        speak("SMS कमांड भेज दी गई। डिलीवरी की पुष्टि फोन नेटवर्क पर निर्भर है।")
    else:
        speak("SMS भेजने में समस्या आई। SMS permission जाँचें।")

def show_help():
    print("""
कमांड उदाहरण:
  "YouTube kholo"       — YouTube खोलें
  "WhatsApp kholo"      — WhatsApp खोलें
  "Chrome kholo"        — Chrome खोलें
  "Google kholo"        — Google खोलें
  "SMS bhejo"           — पुष्टि के साथ SMS लिखें/भेजें
  "time batao"          — समय बताए
  "help"                — कमांड सूची
  "exit" / "band ho jao"— बाहर निकलें

मैसेज ऐप्स के अंदर स्वतः टैप/भेजने की सुविधा Android permissions और ऐप प्रतिबंधों पर निर्भर है।
IRESH किसी भी arbitrary shell command को voice input से execute नहीं करता।
""")

def handle(text):
    t = text.strip().lower()
    if not t:
        return True
    if t in {"exit", "quit", "stop", "band ho jao", "बंद हो जाओ", "बाहर निकलो"}:
        speak("IRESH AI बंद हो रहा है।")
        return False
    if t in {"help", "madad", "commands", "कमांड", "मदद"} or "help" in t:
        show_help()
        return True
    if "time" in t or "समय" in t or "टाइम" in t:
        speak("अभी समय " + time.strftime("%I:%M %p"))
        return True
    if "whatsapp" in t and any(x in t for x in ("open", "khol", "खोल")):
        open_app("com.whatsapp", "WhatsApp")
        return True
    if ("youtube" in t or "यूट्यूब" in t) and any(x in t for x in ("open", "khol", "खोल")):
        open_app("com.google.android.youtube", "YouTube")
        return True
    if ("chrome" in t or "क्रोम" in t) and any(x in t for x in ("open", "khol", "खोल")):
        open_app("com.android.chrome", "Chrome")
        return True
    if "google" in t and any(x in t for x in ("open", "khol", "खोल", "search", "सर्च")):
        open_url("https://www.google.com", "Google")
        return True
    if "sms" in t or "एसएमएस" in t or "text message" in t:
        send_sms_flow()
        return True
    if any(x in t for x in ("search", "सर्च करो", "खोजो")):
        query = re.sub(r"(?i)^(search|google|सर्च करो|खोजो)\s*", "", text).strip()
        if not query:
            query = input("क्या खोजें? ").strip()
        if query:
            open_url("https://www.google.com/search?q=" + urllib.parse.quote_plus(query), "Search")
        return True
    speak("यह कमांड अभी उपलब्ध नहीं है। help बोलें या टाइप करें।")
    return True

def main():
    os.system("clear")
    print(f"""
╔══════════════════════════════════════╗
║          {APP_NAME:^20}      ║
║          Termux Edition v{VERSION}       ║
╚══════════════════════════════════════╝
Hindi/English voice assistant
""")
    if not shutil.which("termux-speech-to-text"):
        print("[i] Voice input के लिए Termux:API app + termux-api package आवश्यक है।")
    show_help()
    speak("नमस्ते! IRESH AI तैयार है।")
    while True:
        try:
            mode = input("\nEnter = voice command | type = text | q = exit: ").strip().lower()
            if mode == "q":
                handle("exit")
                break
            if mode:
                text = mode
            else:
                text = listen()
            if not handle(text):
                break
        except KeyboardInterrupt:
            print("\nCtrl+C — बाहर निकल रहे हैं।")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()

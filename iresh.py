#!/usr/bin/env python3
# IRESH AI v2 — Termux voice assistant
# WhatsApp drafts open in WhatsApp; the user must tap Send.
import os, re, shutil, subprocess, sys, time, urllib.parse

APP = "IRESH AI"
VERSION = "2.0.0"

def run(args, capture=False, timeout=45):
    try:
        return subprocess.run(args, text=True, capture_output=capture, timeout=timeout, check=False)
    except FileNotFoundError:
        print(f"[!] Command not found: {args[0]}")
    except subprocess.TimeoutExpired:
        print("[!] Command timed out.")
    return None

def speak(text):
    print(f"\n{APP}: {text}")
    if shutil.which("termux-tts-speak"):
        run(["termux-tts-speak", text], timeout=30)

def listen():
    if not shutil.which("termux-speech-to-text"):
        speak("Voice tool missing. Install Termux API app and package.")
        return ""
    print("\n🎙️ सुन रहा हूँ... बोलिए।")
    r = run(["termux-speech-to-text"], capture=True, timeout=60)
    text = (r.stdout or "").strip() if r else ""
    if text:
        print("आप:", text)
    else:
        print("[i] आवाज़ पहचानी नहीं गई। दोबारा कोशिश करें।")
    return text

def launch_package(package, label):
    # Uses Android's launcher intent through monkey; package names are allow-listed below.
    r = run(["monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"], capture=True)
    if r and r.returncode == 0:
        speak(f"{label} खोल रहा हूँ।")
    else:
        speak(f"{label} नहीं खुल पाया। ऐप इंस्टॉल है या package name अलग है।")

APPS = {
    "whatsapp": ("com.whatsapp", "WhatsApp"),
    "youtube": ("com.google.android.youtube", "YouTube"),
    "chrome": ("com.android.chrome", "Chrome"),
    "settings": ("com.android.settings", "Settings"),
    "gmail": ("com.google.android.gm", "Gmail"),
    "instagram": ("com.instagram.android", "Instagram"),
    "telegram": ("org.telegram.messenger", "Telegram"),
    "maps": ("com.google.android.apps.maps", "Google Maps"),
    "play store": ("com.android.vending", "Play Store"),
}

def open_url(url):
    if shutil.which("termux-open-url"):
        run(["termux-open-url", url])
    else:
        speak("termux-open-url नहीं मिला।")

def whatsapp_message():
    speak("जिस व्यक्ति को संदेश भेजना है उसका WhatsApp नंबर country code सहित टाइप करें। उदाहरण: 919876543210")
    number = input("WhatsApp number (digits only, country code सहित): ").strip().replace(" ", "").replace("-", "")
    number = number.lstrip("+")
    if not re.fullmatch(r"[0-9]{8,15}", number):
        speak("नंबर सही नहीं है। रद्द किया।")
        return
    speak("अब संदेश बोलें या टाइप करें।")
    mode = input("संदेश बोलने के लिए Enter, टाइप करने के लिए text लिखें: ").strip()
    message = mode if mode else listen()
    if not message.strip():
        speak("संदेश खाली है। रद्द किया।")
        return
    print("\nWhatsApp नंबर:", number)
    print("संदेश:", message)
    confirm = input("WhatsApp में संदेश तैयार करने के लिए OPEN लिखें (भेजने से पहले WhatsApp में जाँचें): ").strip()
    if confirm != "OPEN":
        speak("रद्द कर दिया।")
        return
    url = "https://wa.me/" + number + "?text=" + urllib.parse.quote(message)
    open_url(url)
    speak("WhatsApp खुलना चाहिए और संदेश तैयार होगा। प्राप्तकर्ता और संदेश जाँचकर Send बटन आप स्वयं दबाएँ।")

def google_search(original):
    q = re.sub(r"(?i)^\s*(search|google|सर्च करो|खोजो)\s*", "", original).strip()
    if not q:
        q = input("क्या खोजें? ").strip()
    if q:
        open_url("https://www.google.com/search?q=" + urllib.parse.quote_plus(q))
        speak("Google पर खोज खोल रहा हूँ।")

def help_text():
    print("""
कमांड (बोलें या टाइप करें):
  WhatsApp kholo / YouTube kholo / Chrome kholo
  Instagram kholo / Gmail kholo / Telegram kholo
  Settings kholo / Maps kholo / Play Store kholo
  WhatsApp message bhejo  — नंबर + संदेश; फिर OPEN confirmation
  Google kholo / search Free Fire tips
  time batao
  Hey Iresh              — wake-word mode चालू/फिर से सुनना
  wake off               — wake-word mode बंद
  help
  exit / band ho jao

Wake-word note: यह Termux speech recognizer को बार-बार चलाकर "Hey Iresh" खोजता है।
यह असली always-on/offline hotword engine नहीं है; इंटरनेट/Android speech service की जरूरत हो सकती है
और बैटरी खर्च होगी। Android की अनुमति के बिना यह बैकग्राउंड में भरोसेमंद ढंग से नहीं चलेगा।
""")

def match_open_app(t):
    # Specific allow-list only; no arbitrary shell commands.
    open_words = ("open", "khol", "खोल", "chalao", "चलाओ")
    if not any(w in t for w in open_words):
        return False
    aliases = {
        "whatsapp": "whatsapp", "व्हाट्सएप": "whatsapp",
        "youtube": "youtube", "यूट्यूब": "youtube",
        "chrome": "chrome", "क्रोम": "chrome",
        "settings": "settings", "सेटिंग": "settings", "सेटिंग्स": "settings",
        "gmail": "gmail", "जीमेल": "gmail",
        "instagram": "instagram", "इंस्टाग्राम": "instagram",
        "telegram": "telegram", "टेलीग्राम": "telegram",
        "maps": "maps", "मैप": "maps", "नक्शा": "maps",
        "play store": "play store", "प्ले स्टोर": "play store",
    }
    for alias, key in aliases.items():
        if alias in t and key in APPS:
            launch_package(*APPS[key])
            return True
    return False

def handle(text):
    t = text.strip().lower()
    if not t:
        return True
    if t in ("exit", "quit", "stop", "band ho jao", "बंद हो जाओ", "बाहर निकलो"):
        speak("IRESH AI बंद हो रहा है।")
        return False
    if t in ("help", "madad", "commands", "मदद") or "help" in t:
        help_text()
        return True
    if t in ("wake off", "wake stop", "वेक ऑफ"):
        speak("Wake-word mode command loop में बंद है।")
        return True
    if "time" in t or "समय" in t or "टाइम" in t:
        speak("अभी समय " + time.strftime("%I:%M %p"))
        return True
    if ("whatsapp" in t or "व्हाट्सएप" in t) and any(x in t for x in ("message", "msg", "bhej", "भेज", "मैसेज", "संदेश")):
        whatsapp_message()
        return True
    if "google" in t and any(x in t for x in ("open", "khol", "खोल")):
        open_url("https://www.google.com")
        speak("Google खोल रहा हूँ।")
        return True
    if any(x in t for x in ("search", "सर्च करो", "खोजो")):
        google_search(text)
        return True
    if match_open_app(t):
        return True
    speak("यह कमांड समझ नहीं आई। help बोलकर कमांड सूची देखें।")
    return True

def wake_loop():
    speak("Hey Iresh wake-word mode चालू है। बोलें Hey Iresh, फिर अपनी कमांड बोलें। रोकने के लिए Ctrl+C दबाएँ।")
    while True:
        heard = listen()
        if not heard:
            continue
        low = heard.lower().strip()
        if "hey iresh" in low or "hey irish" in low or "हे इरेश" in low or "हेय इरेश" in low:
            remainder = re.sub(r"(?i)hey\s+(iresh|irish)", "", heard).strip(" ,.!?")
            remainder = remainder.replace("हे इरेश", "").strip(" ,.!?")
            speak("जी, बोलिए।")
            if remainder:
                if not handle(remainder):
                    return
            else:
                command = listen()
                if not handle(command):
                    return
        elif low in ("exit", "quit", "band ho jao", "बंद हो जाओ"):
            return

def main():
    os.system("clear")
    print(f"{APP} — Termux Edition v{VERSION}")
    print("Hindi/English voice assistant")
    help_text()
    speak("नमस्ते! IRESH AI तैयार है।")
    while True:
        try:
            mode = input("\nEnter = voice | command type करें | w = Hey Iresh wake-word mode | q = exit: ").strip()
            if mode.lower() == "q":
                break
            if mode.lower() == "w":
                wake_loop()
                continue
            command = mode if mode else listen()
            if not handle(command):
                break
        except KeyboardInterrupt:
            print("\nबंद किया गया।")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()

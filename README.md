# 🦾 J.A.R.V.I.S — Full Upgrade Edition

> **Just A Rather Very Intelligent System** — Iron Man-style AI assistant with all upgrades enabled.

---

## ✨ Features

| Upgrade | Technology | Status |
|---|---|---|
| 🎙 Wake Word ("Hey JARVIS") | Picovoice Porcupine | ✅ |
| 🧠 AI Brain | Anthropic Claude (Sonnet) | ✅ |
| 👂 Voice Input | OpenAI Whisper (local) | ✅ |
| 🗣 Premium Voice | ElevenLabs TTS | ✅ |
| 🖥 HUD Overlay | PyQt5 Iron Man GUI | ✅ |
| 💾 Long-term Memory | ChromaDB vector store | ✅ |
| 🌐 Web Search | Tavily API | ✅ |
| 🏠 Smart Home | Home Assistant API | ✅ |
| 📱 App Launcher | Cross-platform | ✅ |
| 📊 System Stats | psutil | ✅ |

---

## 📁 Project Structure

```
jarvis/
├── main.py              ← Entry point — run this
├── setup.py             ← One-click installer
├── requirements.txt     ← All dependencies
├── .env.example         ← API key template
├── .env                 ← Your keys (gitignored!)
│
├── config/
│   └── settings.py      ← Config loader
│
├── core/
│   ├── brain.py         ← Claude AI integration
│   ├── ears.py          ← Speech-to-text (Whisper/Google)
│   ├── voice.py         ← Text-to-speech (ElevenLabs/pyttsx3)
│   ├── wake_word.py     ← "Hey JARVIS" detection
│   └── memory.py        ← ChromaDB long-term memory
│
├── skills/
│   └── skills.py        ← Commands: time, apps, search, smart home
│
├── gui/
│   └── hud.py           ← PyQt5 Iron Man HUD
│
├── data/
│   └── memory_db/       ← ChromaDB persistent storage (auto-created)
│
└── sounds/              ← Place custom .wav files here
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
cd jarvis
python setup.py
```

### 2. Add your API keys to `.env`
```env
ANTHROPIC_API_KEY=sk-ant-...          # Required — get at console.anthropic.com
ELEVENLABS_API_KEY=...                # Optional — elevenlabs.io
ELEVENLABS_VOICE_ID=...               # Optional — your chosen voice
PICOVOICE_ACCESS_KEY=...              # Optional — picovoice.ai (free tier)
TAVILY_API_KEY=tvly-...               # Optional — tavily.com (free tier)
HOME_ASSISTANT_URL=http://...         # Optional — your HA instance
HOME_ASSISTANT_TOKEN=...             # Optional — HA long-lived token
```

### 3. Run JARVIS
```bash
python main.py
```

---

## 🎤 Voice Commands

| Say... | JARVIS does... |
|---|---|
| "Hey JARVIS" | Wakes up and listens |
| "What time is it?" | Tells current time/date |
| "System status" | CPU, RAM, battery report |
| "Open YouTube" | Opens in browser |
| "Open Spotify" | Launches app |
| "Turn on the lights" | Smart home control |
| "Search for [topic]" | Web search via Tavily |
| "What's the latest news on X?" | Web search + AI summary |
| "Goodbye JARVIS" | Shuts down gracefully |
| Anything else | Claude AI responds |

---

## 🔑 Getting API Keys

### Anthropic (Required)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create API key → copy to `ANTHROPIC_API_KEY`

### ElevenLabs (Premium Voice)
1. Sign up at [elevenlabs.io](https://elevenlabs.io) (free tier available)
2. Go to **Profile → API Key**
3. Choose a voice (e.g., "Daniel" for British male) → copy Voice ID

### Picovoice (Wake Word)
1. Sign up at [picovoice.ai](https://picovoice.ai) (free tier available)
2. Copy your Access Key
3. The "jarvis" keyword is built-in — no custom training needed!

### Tavily (Web Search)
1. Sign up at [tavily.com](https://tavily.com) (free tier: 1000 searches/month)
2. Copy API key

### Home Assistant (Smart Home)
1. Open Home Assistant → Profile → **Long-Lived Access Tokens**
2. Create token → copy to `HOME_ASSISTANT_TOKEN`
3. Set `HOME_ASSISTANT_URL` to your HA address

---

## ⚙️ Configuration

Edit `.env` to toggle features:

```env
USE_ELEVENLABS=true     # false = use free pyttsx3 voice
USE_WAKE_WORD=true      # false = always listening
USE_SMART_HOME=false    # true = enable Home Assistant
USE_WEB_SEARCH=true     # false = disable Tavily
USE_GUI=true            # false = headless/terminal mode
USE_WHISPER=true        # false = use Google STT (requires internet)
WHISPER_MODEL=base      # tiny/base/small/medium/large (larger = more accurate)
USER_NAME=Sir           # How JARVIS addresses you
```

---

## 🎨 HUD Features

- **Animated arc reactor** — pulsing Iron Man-style decoration
- **Status badges** — LISTENING / THINKING / STANDBY / IDLE
- **Live clock** — always visible
- **Conversation log** — color-coded (your messages vs JARVIS)
- **Text input** — type if you prefer not to speak
- **MIC button** — trigger voice input manually

---

## 💡 Tips

- **Raspberry Pi**: JARVIS runs well on a Pi 4 with USB microphone. Use `USE_GUI=false` for headless mode.
- **Custom wake word**: Create your own at [picovoice.ai/console](https://picovoice.ai/console) (free for personal use).
- **Better voice**: ElevenLabs "Daniel" or "George" voices sound very JARVIS-like.
- **Startup sound**: Place a `boot.wav` in the `sounds/` folder and add `pygame.mixer.music.load('sounds/boot.wav')` to `main.py`.
- **Memory**: JARVIS remembers past conversations using ChromaDB. The database is stored in `data/memory_db/`.

---

## 🛠 Troubleshooting

**"PyAudio install fails"**
```bash
# Windows:
pip install pipwin && pipwin install pyaudio

# macOS:
brew install portaudio && pip install pyaudio

# Linux:
sudo apt install portaudio19-dev && pip install pyaudio
```

**"JARVIS can't hear me"**
- Check microphone permissions in OS settings
- Increase `recognizer.energy_threshold` in `core/ears.py`

**"No module named PyQt5"**
```bash
pip install PyQt5 PyQt5-Qt5 PyQt5-sip
```

---

*Built with ❤️ and Arc Reactor power.*

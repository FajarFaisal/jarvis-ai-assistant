#!/usr/bin/env python3
"""
JARVIS Setup Script — installs dependencies and guides API key setup
Run: python setup.py
"""
import subprocess, sys, os, shutil

def run(cmd):
    print(f"  >> {cmd}")
    return subprocess.run(cmd, shell=True).returncode

def check(package):
    return shutil.which(package) is not None

print("""
╔══════════════════════════════════════════════════════╗
║          J.A.R.V.I.S  —  SETUP WIZARD               ║
╚══════════════════════════════════════════════════════╝
""")

# 1. Python version check
print(f"[1/5] Python {sys.version}")
if sys.version_info < (3, 10):
    print("❌  Python 3.10+ required.")
    sys.exit(1)
print("✅  Python OK")

# 2. pip upgrade
print("\n[2/5] Upgrading pip...")
run(f"{sys.executable} -m pip install --upgrade pip")

# 3. Install requirements
print("\n[3/5] Installing requirements (this may take a few minutes)...")
result = run(f"{sys.executable} -m pip install -r requirements.txt")
if result != 0:
    print("⚠️   Some packages failed. Check errors above.")
else:
    print("✅  All packages installed.")

# 4. Download Whisper model
print("\n[4/5] Downloading Whisper 'base' model (~150 MB)...")
try:
    import whisper
    whisper.load_model("base")
    print("✅  Whisper model ready.")
except Exception as e:
    print(f"⚠️   Whisper setup skipped: {e}")

# 5. Create .env
print("\n[5/5] Setting up configuration...")
if not os.path.exists(".env"):
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅  Created .env from template.")
    else:
        print("⚠️   .env.example not found.")
else:
    print("✅  .env already exists.")

print("""
╔══════════════════════════════════════════════════════╗
║  SETUP COMPLETE!                                     ║
║                                                      ║
║  Next steps:                                         ║
║  1. Open .env and add your API keys:                 ║
║     - ANTHROPIC_API_KEY   (required)                 ║
║     - ELEVENLABS_API_KEY  (premium voice)            ║
║     - PICOVOICE_ACCESS_KEY (wake word)               ║
║     - TAVILY_API_KEY      (web search)               ║
║     - HOME_ASSISTANT_*    (smart home)               ║
║                                                      ║
║  2. Run JARVIS:                                      ║
║       python main.py                                 ║
║                                                      ║
║  3. Say "Hey JARVIS" or type in the HUD              ║
╚══════════════════════════════════════════════════════╝
""")

"""
JARVIS — Main Entry Point
Ties together: wake word → listen → route/think → speak → GUI
"""
import sys, os, threading, time
sys.path.insert(0, os.path.dirname(__file__))

from config.settings   import USE_GUI, USE_WAKE_WORD, USER_NAME, JARVIS_NAME
from core.brain        import JARVISBrain
from core.voice        import speak
from core.ears         import listen
from core.wake_word    import WakeWordDetector
from core.memory       import recall, remember_exchange
from skills.skills     import route, web_search

# ── Optional GUI ─────────────────────────────────────────────────────
window = None

def _try_import_gui():
    global window
    if not USE_GUI:
        return
    try:
        from PyQt5.QtWidgets import QApplication
        from gui.hud import JARVISWindow
        app = QApplication.instance() or QApplication(sys.argv)
        window = JARVISWindow()
        window.show()
        return app
    except Exception as e:
        print(f"[JARVIS] GUI unavailable: {e}. Running headless.")
        return None


def gui_log_user(text):
    if window:
        window.show_user(text)

def gui_log_jarvis(text):
    if window:
        window.show_jarvis(text)

def gui_log_sys(text):
    if window:
        window.show_system(text)

def gui_listening(val):
    if window:
        window.set_listening(val)

def gui_thinking(val):
    if window:
        window.set_thinking(val)


# ── Core Loop ─────────────────────────────────────────────────────────
brain        = JARVISBrain()
_wake_event  = threading.Event()
_running     = True


def process_input(user_text: str):
    """Handle one turn: route or think, then speak."""
    if not user_text.strip():
        return

    print(f"\n[You] {user_text}")
    gui_log_user(user_text)

    # 1. Try local skill routing first
    response, handled = route(user_text)

    if not handled:
        gui_thinking(True)

        # 2. Retrieve relevant memories for context
        memories = recall(user_text, n=2)
        context = "\n".join(memories) if memories else ""

        # 3. Maybe search the web for current info
        search_keywords = ["latest", "news", "today", "current", "who is", "what is", "when is", "price"]
        if any(k in user_text.lower() for k in search_keywords):
            gui_log_sys("Searching the web...")
            search_ctx = web_search(user_text)
            if search_ctx:
                context = (context + "\n" + search_ctx).strip()

        # 4. Ask Claude
        response = brain.think(user_text, context=context)
        gui_thinking(False)

    # 5. Store exchange in memory
    remember_exchange(user_text, response)

    # 6. Output
    print(f"[{JARVIS_NAME}] {response}\n")
    gui_log_jarvis(response)
    speak(response)


def voice_loop():
    """Continuous voice input loop."""
    while _running:
        if USE_WAKE_WORD:
            gui_log_sys("Waiting for wake word...")
            _wake_event.wait()
            _wake_event.clear()

        gui_listening(True)
        user_text = listen(timeout=6, phrase_limit=20)
        gui_listening(False)

        if user_text:
            # Graceful shutdown command
            if any(w in user_text.lower() for w in ["goodbye jarvis", "shutdown jarvis", "power down"]):
                farewell = f"Goodbye, {USER_NAME}. Powering down. Stay safe."
                speak(farewell)
                gui_log_jarvis(farewell)
                time.sleep(2)
                os._exit(0)

            process_input(user_text)


def on_wake_word():
    speak(f"Yes, {USER_NAME}?", silent=False)
    _wake_event.set()


def main():
    global _running

    # ── Startup ──────────────────────────────────────────────────────
    print("=" * 60)
    print(f"  {JARVIS_NAME} — Initializing all systems...")
    print("=" * 60)

    # GUI
    qt_app = _try_import_gui()
    gui_log_sys("JARVIS online.")

    # Boot greeting
    greeting = (
        f"Good {_time_of_day()}, {USER_NAME}. "
        f"All systems are online. "
        f"{'Wake word detection is active. Say Hey JARVIS to begin.' if USE_WAKE_WORD else 'Listening for your command.'}"
    )
    speak(greeting)
    gui_log_jarvis(greeting)

    # Wake word
    detector = WakeWordDetector(callback=on_wake_word)
    detector.start()

    # Hook GUI text input
    if window:
        window.text_callback = process_input
        window.mic_callback  = lambda: threading.Thread(
            target=lambda: process_input(listen()), daemon=True
        ).start()

    # Start voice loop in background thread
    voice_thread = threading.Thread(target=voice_loop, daemon=True)
    voice_thread.start()

    # ── Event loop ────────────────────────────────────────────────────
    if qt_app and window:
        sys.exit(qt_app.exec_())
    else:
        # Headless: keyboard input fallback
        print("\nHeadless mode. Type your commands (or 'quit' to exit):\n")
        while True:
            try:
                user_input = input(f"{USER_NAME}: ").strip()
                if user_input.lower() in ("quit", "exit", "bye"):
                    speak(f"Goodbye, {USER_NAME}.")
                    break
                if user_input:
                    process_input(user_input)
            except (EOFError, KeyboardInterrupt):
                break


def _time_of_day() -> str:
    hour = time.localtime().tm_hour
    if hour < 12:  return "morning"
    if hour < 17:  return "afternoon"
    return "evening"


if __name__ == "__main__":
    main()

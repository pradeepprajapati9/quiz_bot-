"""Config for the GK quiz bot."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except Exception:
    pass

BASE_DIR = Path(__file__).parent
BACKLOG_FILE = BASE_DIR / "backlog.json"   # pre-generated questions
STATE_FILE = BASE_DIR / "state.json"       # asked-question fingerprints
LOG_FILE = BASE_DIR / "bot.log"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
QUIZ_LANG = os.getenv("QUIZ_LANG", "hi").lower()
DO_POST = os.getenv("DO_POST", "false").lower() == "true"

BACKLOG_MIN = int(os.getenv("BACKLOG_MIN", "10"))
PER_REFILL = int(os.getenv("PER_REFILL", "12"))

# Exam-relevant categories rotated for variety.
CATEGORIES = [
    "Indian History", "Indian Geography", "Indian Polity & Constitution",
    "General Science (Physics, Chemistry, Biology)", "Static GK (awards, days, books)",
    "World Geography", "Economics basics", "Sports GK", "Famous personalities",
    "Indian culture & festivals",
]

"""Post a native Telegram QUIZ poll to the channel."""
import json
import requests
import config


def post_quiz(q: dict) -> bool:
    if not config.DO_POST:
        print("=== DRY-RUN quiz ===")
        print("Q:", q["question"])
        for i, o in enumerate(q["options"]):
            print(f"  {'✓' if i == q['correct'] else ' '} {o}")
        print("explain:", q.get("explanation", ""), "\n")
        return True
    if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHANNEL):
        print("[telegram] missing token / channel")
        return False
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendPoll"
    data = {
        "chat_id": config.TELEGRAM_CHANNEL,
        "question": q["question"],
        "options": json.dumps([{"text": o} for o in q["options"]]),
        "type": "quiz",
        "correct_option_id": q["correct"],
        "is_anonymous": True,
    }
    if q.get("explanation"):
        data["explanation"] = q["explanation"]
    try:
        r = requests.post(url, timeout=30, data=data)
        if r.status_code == 200 and r.json().get("ok"):
            print("[telegram] quiz posted ✓")
            return True
        print(f"[telegram] failed: {r.status_code} {r.text[:200]}")
    except Exception as ex:
        print(f"[telegram] error: {ex}")
    return False

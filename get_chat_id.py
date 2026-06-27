"""Find your quiz channel's chat_id. Add the bot as admin, post any message in
the channel, put the token in .env, then run:  python get_chat_id.py"""
import requests
import config

if not config.TELEGRAM_BOT_TOKEN:
    print("Put TELEGRAM_BOT_TOKEN in .env first.")
    raise SystemExit(1)
data = requests.get(
    f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/getUpdates", timeout=30).json()
found = {}
for u in data.get("result", []):
    chat = (u.get("channel_post") or u.get("edited_channel_post") or {}).get("chat") \
        or (u.get("my_chat_member") or {}).get("chat")
    if chat and chat.get("type") == "channel":
        found[chat["id"]] = chat.get("title", "")
if found:
    for cid, title in found.items():
        print(f"  TELEGRAM_CHANNEL={cid}    ({title})")
else:
    print("No channel post found. Add bot as admin, post a message, then re-run.")
    print(data)

# 🧠 GK Quiz Bot (Telegram, free)

Posts native **interactive quiz polls** (GK for Indian exam aspirants) to your
Telegram channel - Gemini writes the questions, the bot keeps a backlog and posts
a few per day automatically. Grow a channel -> monetize via promotions/sponsorships.

## Setup
1. **Telegram channel** for quizzes; add your bot (e.g. the existing one) as **Admin**.
2. Put the bot token in `.env`, post a message in the channel, run
   `python get_chat_id.py` to get the channel id.
3. Fill `.env`: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL`, `GEMINI_API_KEY`.
4. Test: `python main.py` (DO_POST=false = dry-run). Then set `DO_POST=true`.
5. Push to a GitHub repo; add the same as **Actions secrets**
   (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL`, `GEMINI_API_KEY`). It posts 3 quizzes/day.

## How it works
```
Gemini writes GK MCQs (backlog) -> post next as a native Telegram quiz poll
-> users tap an answer, see correct + explanation -> engagement -> channel grows
```
Language: `QUIZ_LANG=hi` (Hindi) or `en`. No web hosting needed.

"""GK Quiz bot: posts one native Telegram quiz poll per run.

  keep a backlog of Gemini-generated questions -> post the next unused one
  as an interactive quiz poll -> mark it used. Run a few times a day via cron.
"""
import sys
import json
import traceback
from datetime import datetime

import config
import quiz_gen
import telegram

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def log(msg):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line)
    try:
        with open(config.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def _load():
    if config.BACKLOG_FILE.exists():
        try:
            return json.loads(config.BACKLOG_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"questions": []}


def _save(d):
    config.BACKLOG_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), "utf-8")


def top_up(data):
    unused = [q for q in data["questions"] if not q.get("posted")]
    if len(unused) >= config.BACKLOG_MIN:
        return
    asked = [q["question"] for q in data["questions"]]
    seen = {q["question"].strip().lower() for q in data["questions"]}
    fresh = quiz_gen.generate(asked, config.PER_REFILL)
    added = 0
    for q in fresh:
        if q["question"].strip().lower() in seen:
            continue
        seen.add(q["question"].strip().lower())
        q["posted"] = False
        data["questions"].append(q)
        added += 1
    data["questions"] = data["questions"][-400:]   # bound size
    if added:
        _save(data)
    log(f"backlog +{added} (unused now {sum(1 for q in data['questions'] if not q.get('posted'))})")


def run():
    data = _load()
    top_up(data)
    nxt = next((q for q in data["questions"] if not q.get("posted")), None)
    if not nxt:
        log("No question available (Gemini issue). Try again later.")
        return
    log(f"Posting quiz: {nxt['question'][:60]}")
    if telegram.post_quiz(nxt):
        nxt["posted"] = True
        _save(data)
        log("Done.")
    else:
        log("Post failed (will retry next run).")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        log("ERROR:\n" + traceback.format_exc())
        sys.exit(1)

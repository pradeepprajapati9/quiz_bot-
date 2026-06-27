"""Generate GK quiz questions with Gemini (free, resilient)."""
import re
import json
import time
import random
import requests
import config

MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-flash-lite"]


def _gemini(prompt: str) -> str:
    if not config.GEMINI_API_KEY:
        return ""
    for attempt in range(2):
        for model in MODELS:
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{model}:generateContent?key={config.GEMINI_API_KEY}")
            try:
                r = requests.post(url, timeout=60,
                                  json={"contents": [{"parts": [{"text": prompt}]}]})
                if r.status_code == 200:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
                if r.status_code in (429, 503):
                    continue
            except Exception as ex:
                print(f"[quiz] {model} error: {ex}")
        if attempt == 0:
            time.sleep(3)
    return ""


def generate(avoid: list[str], n: int) -> list[dict]:
    lang = "Hindi" if config.QUIZ_LANG == "hi" else "English"
    cat = random.choice(config.CATEGORIES) if False else config.CATEGORIES[
        sum(ord(c) for c in (avoid[-1] if avoid else "x")) % len(config.CATEGORIES)]
    skip = "; ".join(avoid[-50:]) or "none"
    prompt = (
        f"Create {n} multiple-choice General Knowledge quiz questions in {lang} for "
        f"Indian competitive-exam aspirants (SSC, Banking, Railway). Topic focus: {cat}. "
        f"Factually ACCURATE, exam-style, not too easy. Do NOT repeat: {skip}.\n"
        f"Return ONLY a valid JSON array, each item exactly:\n"
        f'{{"question": "...", "options": ["..","..","..",".."], "correct": 0, '
        f'"explanation": "..."}}\n'
        f"Rules: exactly 4 options; 'correct' = 0-based index of the right option; "
        f"question <= 200 chars; each option <= 90 chars; explanation = 1 short {lang} "
        f"sentence (<160 chars) telling why. Plain text, no markdown."
    )
    raw = _gemini(prompt)
    if not raw:
        return []
    try:
        raw = raw[raw.find("["): raw.rfind("]") + 1]
        raw = re.sub(r",\s*([}\]])", r"\1", raw)
        items = json.loads(raw)
    except Exception as ex:
        print(f"[quiz] parse failed: {ex}")
        return []
    out = []
    for q in items if isinstance(items, list) else []:
        opts = q.get("options") or []
        if (q.get("question") and isinstance(opts, list) and len(opts) == 4
                and isinstance(q.get("correct"), int) and 0 <= q["correct"] <= 3):
            out.append({
                "question": q["question"].strip()[:295],
                "options": [str(o).strip()[:99] for o in opts],
                "correct": q["correct"],
                "explanation": (q.get("explanation") or "").strip()[:195],
            })
    return out

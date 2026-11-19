# translate.py
# Turns the text from stt.py into English. Used by app.py and phase5_check.py.

import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

TIMEOUT_SECONDS = 5       # one translator call may take at most this long
SLOW_SECONDS = 2          # slower than this gets a "slow" flag

MESSAGES = {
    "unsupported": "I cannot understand this language yet. Let me connect you to a person.",
    "trouble": "I am having trouble. Let me connect you to a person.",
}

# words we expect to see in a banking sentence
BANKING_WORDS = ["card", "account", "balance", "loan", "branch", "ifsc", "upi", "pin", "otp",
                 "kyc", "emi", "block", "lost", "transaction", "payment", "limit", "bank",
                 "money", "atm", "debit", "credit", "fraud", "activate", "statement",
                 "delivery", "dispatch", "amount"]

# for each language: the code Google wants, and the name MyMemory wants
# Manipuri (mni) is not here on purpose, so it gets the "unsupported" message
CODES = {
    "hi": ["hi", "hindi"],
    "mr": ["mr", "marathi"],
    "ta": ["ta", "tamil"],
    "te": ["te", "telugu"],
    "kn": ["kn", "kannada"],
    "bn": ["bn", "bengali"],
    "ur": ["ur", "urdu"],
    "es": ["es", "spanish"],
    "ru": ["ru", "russian"],
    "raj": ["hi", "hindi"],     # Rajasthani goes through the Hindi setting
}

glossary_path = os.path.join(os.path.dirname(__file__), "glossary.json")
with open(glossary_path, encoding="utf-8") as f:
    GLOSSARY = json.load(f)

cache = {}                # remembers sentences we already translated
blocked_until = {}        # translator name -> time when we may try it again
BLOCK_SECONDS = 120       # a translator that just failed is skipped for this long


def google(text, lang):
    from deep_translator import GoogleTranslator
    return GoogleTranslator(source=CODES[lang][0], target="en").translate(text)


def mymemory(text, lang):
    from deep_translator import MyMemoryTranslator
    answer = MyMemoryTranslator(source=CODES[lang][1], target="english").translate(text)
    # when the free limit is used up, MyMemory may send a warning text instead of an error
    if "MYMEMORY WARNING" in str(answer).upper():
        raise RuntimeError("MyMemory limit reached")
    return answer


# the order we try them in
ENGINES = [["Google", google], ["MyMemory", mymemory]]


def usable_engines():
    now = time.time()
    ready = [e for e in ENGINES if blocked_until.get(e[0], 0) <= now]
    if len(ready) == 0:       # all of them failed recently, so try them all again
        ready = ENGINES
    return ready


def fix_before(text):
    # write the banking words in English letters before translating
    for native, english in GLOSSARY["before_translation"].items():
        text = text.replace(native, english)
    return text


def fix_after(text):
    # put the banking words right again after translating
    for wrong, right in GLOSSARY["after_translation"].items():
        text = re.sub(r"\b" + wrong + r"\b", right, text, flags=re.I)
    return text


def run_with_timeout(function, text, lang):
    pool = ThreadPoolExecutor(max_workers=1)
    future = pool.submit(function, text, lang)
    try:
        return future.result(timeout=TIMEOUT_SECONDS)
    finally:
        pool.shutdown(wait=False)


def to_english(text, lang):
    result = {"ok": False, "english": "", "engine": "", "seconds": 0.0, "flags": [], "message": ""}

    if text is None or text.strip() == "":
        result["message"] = MESSAGES["trouble"]
        return result

    # English needs no translation, only the banking word fix
    if lang == "en":
        result["english"] = fix_after(text)
        result["engine"] = "none"
        result["ok"] = True
        return result

    if lang not in CODES:
        result["message"] = MESSAGES["unsupported"]
        return result

    key = lang + "|" + text
    if key in cache:
        return dict(cache[key])

    prepared = fix_before(text)
    english = None
    start = time.time()
    for name, function in usable_engines():
        try:
            english = run_with_timeout(function, prepared, lang)
            result["engine"] = name
            break
        except Exception:
            blocked_until[name] = time.time() + BLOCK_SECONDS
            continue          # this translator failed, so try the next one
    result["seconds"] = round(time.time() - start, 2)

    if english is None or english.strip() == "":
        result["message"] = MESSAGES["trouble"]
        return result

    result["english"] = fix_after(english)
    if result["seconds"] > SLOW_SECONDS:
        result["flags"].append("slow")
    lower = result["english"].lower()
    if not any(word in lower for word in BANKING_WORDS):
        result["flags"].append("no_banking_word")
    result["ok"] = True
    cache[key] = dict(result)
    return result
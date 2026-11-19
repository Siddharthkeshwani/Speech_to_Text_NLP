# phase5_check.py
# Runs speech to text and then translation on every clip in the manifest.
# How to run (from the project folder, with (.venv) showing):  python phase5_check.py

import difflib
import os
import re
import sys
import time

import pandas as pd

import stt
import translate

# make the terminal print Hindi / Marathi without crashing
sys.stdout.reconfigure(encoding="utf-8")

manifest = pd.read_csv("data/sample_audio/manifest.csv")
code_of = {cfg["name"]: code for code, cfg in stt.LANGS.items()}   # "Hindi" -> "hi"
TERMS = ["IFSC", "UPI", "PIN", "OTP"]


def simple(text):
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).split())


rows = []
for i, clip in manifest.iterrows():
    lang = code_of[clip["language"]]
    path = "data/sample_audio/" + clip["clip_name"]
    if not os.path.exists(path):
        print(clip["clip_name"], "-> MISSING, skipped")
        continue

    heard = stt.transcribe(path, lang)
    if not heard["ok"]:
        print(clip["clip_name"], "-> speech failed:", heard["message"])
        rows.append({"clip": clip["clip_name"], "language": clip["language"], "heard": "", "english": "",
                     "expected_english": clip["expected_english_text"], "similarity": 0.0, "terms_ok": False,
                     "engine": "", "seconds": 0.0, "flags": "", "passed": False})
        continue

    out = translate.to_english(heard["text"], lang)
    similarity = round(difflib.SequenceMatcher(None, simple(clip["expected_english_text"]), simple(out["english"])).ratio(), 2)

    # every banking term in the expected English must also be in our English
    terms_ok = True
    for term in TERMS:
        if term in clip["expected_english_text"] and term not in out["english"]:
            terms_ok = False

    passed = out["ok"] and similarity >= 0.6 and terms_ok
    rows.append({"clip": clip["clip_name"], "language": clip["language"], "heard": heard["text"],
                 "english": out["english"] or out["message"], "expected_english": clip["expected_english_text"],
                 "similarity": similarity, "terms_ok": terms_ok, "engine": out["engine"],
                 "seconds": out["seconds"], "flags": " ".join(out["flags"]), "passed": passed})
    print(clip["clip_name"], "->", "PASS" if passed else "FAIL", similarity, out["engine"], out["seconds"], "s")

    if lang != "en":
        time.sleep(1)       # a short rest, so the online translator does not block us

if len(rows) == 0:
    print("\nNo clips were processed. Check data/sample_audio/ and manifest.csv.")
    sys.exit()

results = pd.DataFrame(rows)
results.to_csv("docs/phase5_results.csv", index=False)

print("\n=========== CLIP RESULTS ===========")
show = results.copy()
show["heard"] = show["heard"].str.slice(0, 40)
show["english"] = show["english"].str.slice(0, 40)
show["expected_english"] = show["expected_english"].str.slice(0, 40)
print(show[["clip", "english", "expected_english", "similarity", "terms_ok", "engine", "seconds", "flags", "passed"]].to_string(index=False))

print("\n=========== SUMMARY ===========")
summary = results.groupby("language").agg(passed=("passed", "sum"), clips=("passed", "size"),
                                          avg_seconds=("seconds", "mean")).reset_index()
summary["avg_seconds"] = summary["avg_seconds"].round(2)
print(summary.to_string(index=False))
print("\nFull table saved in docs/phase5_results.csv")
# phase4_gate.py
# Runs the Phase 4 decision gate on every clip in data/sample_audio/manifest.csv.
#
# How to run (from the project folder, with (.venv) showing):
#   python phase4_gate.py base            one Whisper size
#   python phase4_gate.py base small      two sizes, one after the other
#   python phase4_gate.py indic           IndicConformer (Hindi and Marathi clips only)

import difflib
import os
import sys
import unicodedata

import pandas as pd

import stt

# make the terminal print Hindi / Marathi without crashing
sys.stdout.reconfigure(encoding="utf-8")

engines = sys.argv[1:] or ["base"]
manifest = pd.read_csv("data/sample_audio/manifest.csv")
code_of = {cfg["name"]: code for code, cfg in stt.LANGS.items()}   # "Hindi" -> "hi"

# the first word of a letter's Unicode name tells us its script
SCRIPT_WORD = {"Latin": "LATIN", "Devanagari": "DEVANAGARI", "Tamil": "TAMIL", "Telugu": "TELUGU",
               "Kannada": "KANNADA", "Bengali": "BENGALI", "Perso-Arabic": "ARABIC",
               "Cyrillic": "CYRILLIC", "Meitei Mayek": "MEETEI"}
PASS_SHARE = 0.66        # a language passes if at least this share of its clips pass


def simple(text):
    # lowercase, keep letters, marks and digits, turn everything else into a space
    kept = ""
    for ch in str(text).lower():
        if unicodedata.category(ch)[0] in "LMN" or ch == " ":
            kept = kept + ch
        else:
            kept = kept + " "
    return " ".join(kept.split())


def script_ok(text, script):
    letters = [ch for ch in text if unicodedata.category(ch).startswith("L")]
    if len(letters) == 0:
        return False
    right = [ch for ch in letters if unicodedata.name(ch, "").startswith(SCRIPT_WORD[script])]
    return len(right) / len(letters) >= 0.8


rows = []
for name in engines:
    print("\nLoading", name, "...")
    if name == "indic":
        stt.get_indic()
    else:
        stt.get_whisper(name)

    for i, clip in manifest.iterrows():
        lang = code_of[clip["language"]]
        cfg = stt.LANGS[lang]
        if name == "indic" and cfg["indic_code"] is None:
            continue                                   # IndicConformer is not used for English
        path = "data/sample_audio/" + clip["clip_name"]
        if not os.path.exists(path):
            print(clip["clip_name"], "-> MISSING, skipped")
            continue
        if name == "indic":
            out = stt.transcribe(path, lang, engine="indic")
        else:
            out = stt.transcribe(path, lang, engine="whisper", size=name)

        expected = simple(clip["expected_native_text"])
        heard = simple(out["text"])
        similarity = round(difflib.SequenceMatcher(None, expected, heard).ratio(), 2)
        right_script = script_ok(out["text"], cfg["script"])
        passed = out["ok"] and right_script and similarity >= 0.6
        rows.append({"engine": out["engine"] or name, "language": clip["language"], "clip": clip["clip_name"],
                     "expected": clip["expected_native_text"], "heard": out["text"] or out["message"],
                     "similarity": similarity, "script_ok": right_script, "seconds": out["seconds"],
                     "avg_logprob": out["avg_logprob"], "passed": passed})
        print(clip["clip_name"], "->", "PASS" if passed else "FAIL", similarity, out["seconds"], "s")

if len(rows) == 0:
    print("\nNo clips were processed. Check data/sample_audio/ and manifest.csv.")
    sys.exit()

results = pd.DataFrame(rows)
results.to_csv("docs/phase4_results.csv", index=False)

print("\n=========== CLIP RESULTS ===========")
show = results.copy()
show["heard"] = show["heard"].str.slice(0, 45)
show["expected"] = show["expected"].str.slice(0, 45)
print(show[["engine", "clip", "expected", "heard", "similarity", "script_ok", "seconds", "passed"]].to_string(index=False))

print("\n=========== GATE SUMMARY ===========")
summary = results.groupby(["engine", "language"]).agg(passed=("passed", "sum"), clips=("passed", "size"),
                                                      avg_seconds=("seconds", "mean")).reset_index()
summary["avg_seconds"] = summary["avg_seconds"].round(2)
summary["verdict"] = ["PASS" if p / c >= PASS_SHARE else "FAIL" for p, c in zip(summary["passed"], summary["clips"])]
print(summary.to_string(index=False))
print("\nFull table saved in docs/phase4_results.csv")
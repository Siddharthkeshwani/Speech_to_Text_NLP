# phase5_timing.py
# Translates one Hindi sentence 10 times and prints how long each call took.
# How to run (from the project folder, with (.venv) showing):  python phase5_timing.py

import sys
import time

import translate

sys.stdout.reconfigure(encoding="utf-8")

sentence = "मेरा कार्ड खो गया है"
times = []

for number in range(1, 11):
    translate.cache.clear()           # forget old answers, so every call is a real call
    out = translate.to_english(sentence, "hi")
    print(number, out["engine"] or "FAILED", out["seconds"], "s", out["english"])
    times.append(out["seconds"])
    time.sleep(1)                     # a short rest between calls

print("\nAverage:", round(sum(times) / len(times), 2), "s")
print("Slowest:", max(times), "s")
print("Calls over 2 seconds:", len([t for t in times if t > 2]), "of", len(times))
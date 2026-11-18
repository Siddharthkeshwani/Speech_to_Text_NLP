# Smoke test results

Date: 16 November 2026
Laptop: HP OMEN 16, 24 GB RAM, Intel Core Ultra 7 255H
Python version: 3.11.9
Run on: CPU only (Whisper printed the "FP16 is not supported on CPU" warning, which is harmless)

| Test | Status | Time | Notes |
| --- | --- | --- | --- |
| Whisper base load | PASS | 65.3 s | First run, so it includes the 139 MB model download. Later runs load faster. |
| Whisper base transcribe (short clip) | PASS | 1.1 s | Heard "My card is lost." and detected the language as `en`. |
| Translation, Hindi to English, Google | FAIL | not measured | Google said "too many requests", even after re-running at different times. |
| Translation, Hindi to English, MyMemory (fallback) | PASS | 1.84 s | One run only. Close to the 2 second target, so treat it as typical, not guaranteed. |
| scikit-learn toy model | PASS | 0.014 s | Predicted `lost` with 41.8% confidence. Low on purpose, because the model learned from only six sentences. |

What this means:

1. Phase 0 is done. All three pieces ran on this laptop.
2. Speech plus translation plus classifier add up to about 3 seconds for a short English-style clip (1.1 + 1.84 + 0.014 = 2.95). That is well inside the 8 second budget in the PRD.
3. The speech time is for Whisper `base` on an English clip. Bigger models for Indian languages (Phase 4 gate) are not measured yet.
4. I did not write down the English text MyMemory returned. Add it here if you remember it, because translation quality matters more than speed.
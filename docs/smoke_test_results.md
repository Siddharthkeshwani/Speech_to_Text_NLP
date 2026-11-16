# Smoke test results

Date: 16 november 2026.
Laptop: HP OMEN 16, 24GB, Ultra 7 255H.
Python version: Python 3.11.9


| Test | Status | Time | Notes |
| --- | --- | --- | --- |
| Whisper base load |Passed | first run includes the download - 65.3 seconds | - |
| Whisper base transcribe (5 s clip) | Passed | 1.1 seconds|-|
| Translation (Hindi to English) | Translation failed:Server Error:too many request|-|-| 
| scikit-learn toy model | Passed |0.014 seconds | Prediction: lost Confidence: 41.8 % |


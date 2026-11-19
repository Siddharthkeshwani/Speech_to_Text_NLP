# Risk list

Date: 17 November 2026
Ratings (Low, Medium, High) are my own judgement. They are not measured.
Status words: Open (not yet dealt with), Happened (it has already occurred), Reduced (a fix is in place), Planned (the fix is scheduled).

| ID | Risk | Why it matters | Likelihood | Impact | Response | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | The training text is written by me | Held-out scores will look better than real use | High | Medium | Grouped split by template, an unseen-phrasing test with new sentences, a live spoken test, and honest reporting | Planned (Phase 3, 6, 9) |
| R2 | Simulated noise differs from real speech-to-text errors | The model may meet error patterns it never saw | High | Medium | Collect real errors from sample clips and add them as new noise patterns | Planned (Phase 4) |
| R3 | Translation errors reach the classifier | One wrong word can change the intent | Medium | High | Show both texts, correction loop, glossary protection for IFSC, UPI, PIN and OTP, noise in training | Planned |
| R4 | The online translator is unreliable and not private | Text leaves the machine, and the service can block you | High | Medium | Timeout, a fallback translator, skip a failed translator for 120 s, an offline option, a privacy notice. | Happened again (18 Nov). Google was blocked in Phase 0 and Phase 5. MyMemory answered all 10 calls at 3.76 s average. |
| R5 | Rajasthani and Manipuri tools are weak or missing | Results may be unreliable | High | Low | Mark experimental, stricter thresholds, native-speaker check | Planned |
| R6 | Hindi and Urdu get confused | Wrong language means a wrong transcript | Medium | Medium | A dropdown that always wins, and a confirm step when the score is low | Planned |
| R7 | Probabilities are overconfident | Lanes depend on trustworthy scores | Medium | High | Check the 0.9 bucket and calibrate | Planned (Phase 6) |
| R8 | Heavy models are slow on a laptop CPU | The app becomes too slow to demo | Medium | Medium | Smaller model sizes, load once, a demo video as a backup | Open. Whisper base took 1.1 s on the Ultra 7 255H. Bigger models are not measured. |
| R9 | The dataset licence is non-commercial (CC BY-NC 4.0, S6) | Limits what can be claimed and shared | Certain | Medium | State it in the README, share scripts and not audio, call it a research prototype | Planned (Phase 10) |
| R10 | Class names assumed wrongly | Lanes would be wrong | Low | High | Read intent_info.csv before assigning lanes | Reduced. The 14 names were checked against the file in Phase 0, and the plan's provisional lanes match them. |
| R11 | A class is missing from the test split | Metrics would hide a weak class | High | Medium | Count templates per class first, then use StratifiedGroupKFold. **In Phase 0 the plan's split on 151 templates left class 1 (activate_card) out of the test set.** | Happened (Phase 0 check). Fix in Phase 3. |
| R12 | Scope creep from 12 languages | Delays the project | High | High | Freeze the list and the tiers in this PRD. Core languages first. | Open |
| R13 | Whisper base is too weak for Indian languages | Transcripts may be mostly wrong (H6, S7, S8) | High | High | The Phase 4 decision gate, with a stronger model if needed | Planned (Phase 4) |
| R14 | The Skit data is Indian English recorded on a phone, not Indian-language speech | The classifier learns English templates, but live input is translated Indian-language speech (S6) | High | Medium | Say it in the data sheet and README. Add noisy and translated-style phrasing in Phase 3. | Planned |
| R15 | The RBI fraud-reporting window is changing and the start date is unclear (S1, S2) | A wrong date in a read-back could mislead a caller | Medium | High | The app does not quote any window. A person does. | Reduced (PRD rule) |
| R16 | There is no primary user research | The README must not claim interviews or user feedback | Certain | Medium | Say "desk research" everywhere. Collect real feedback later if possible. | Reduced (wording rule from Phase 1) |
| R17 | The urgent-class test sets are tiny | A recall percentage would look more precise than it is | High | Medium | Report counts such as "14 of 15" | Planned (Phase 6, 9) |
| R18 | The template count in the plan (164) is wrong after cleaning | The plan's checks say 164 and 2,460 rows | Certain | Low | Use 150 templates and about 2,250 rows (150 x 15). Update the checks. | Happened (Phase 0 check). Fix in Phase 3. |
| R19 | The text of the sample sentences and error messages may sound unnatural in other languages | The caller may not trust the screen | Medium | Medium | A native speaker checks the read-back and error messages | Planned (Phase 7) |
| R20 | Callers say real card, account or phone numbers into the demo | Private data would end up in the text log and with the online translator | Medium | High | A notice on screen, no audio stored, tell testers to use fake numbers | Planned (Phase 8) |
| R21 | MyMemory is a free service with limits | It may slow down, refuse requests or have a daily cap (I did not verify the cap) | Medium | Medium | The 5 s timeout, a cache for repeated sentences, the offline IndicTrans2 route later | Open |
| R22 | The Marathi chain is weak | The speech text is wrong for 2 of 3 clips, and the translator cannot repair it | High | Medium | Marathi is experimental. Try IndicConformer later. Show both texts and send low-confidence clips to a person. | Open |
| R23 | The "cart" and "guide" fixes hide a warning sign | "My card is full of books" now has a banking word, so the no_banking_word flag no longer fires | Medium | Medium | Phase 7 adds a speech check (Whisper's own score) next to the translation check | Planned (Phase 7) |

## Top three to watch

1. R13 (Whisper base on Indian languages), because without a good transcript nothing after it works.
2. R4 (translator), because it has already failed once.
3. R12 (scope creep), because twelve languages is the easiest way to run out of time.
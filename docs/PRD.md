# Product Requirements Document (PRD)

Product: Multilingual Voice Intent Triage for Banking Calls (student prototype)
Version: 1.0
Date: 17 November 2026
Author: (your name)
Review status: self-checked only. A second person has not reviewed it yet (see prd_review.md).

## 1. Summary

Callers to a bank often speak in their own language. This prototype listens to one short clip, shows what it heard in the speaker's own language, translates it to English, and predicts which of 14 banking intents it is (for example "lost card" or "balance"). It then shows how sure it is and decides whether the call can be handled automatically or must go to a person. Every step is visible on screen so a person can check it.

It is a research prototype. It does not take any bank action. It does not connect to a phone line.

Evidence for the problem is desk research only (research_sources.md). No interviews were done.

## 2. What is being built

Priority rule I used:

| Priority | Meaning |
| --- | --- |
| Must | Needed for the project document's required output (speech to text, prediction, confidence), or for safety, or for the demo to work |
| Should | Makes the product trustworthy or useful, but the demo still works without it |
| Could | Optional. Only after all Must items work. |

### 2.1 Feature list

| ID | Feature | Priority | For | Why (evidence or reason) | Done when |
| --- | --- | --- | --- | --- | --- |
| F1 | Record audio in the browser, with a file upload as a backup | Must | Caller, Evaluator | The project document needs speech input (steps 17 and 18). The built-in recorder depends on the installed Streamlit version, so an upload backup is needed. | A clip of about 5 seconds records, plays back, and is passed on |
| F2 | Language choice: a dropdown that always wins, with auto-detect only where the speech tool supports it | Must | Caller | Hindi and Urdu sound alike, so detection alone is not enough (plan). Language preference in India is strong but the evidence is indirect (H1, S4). | The dropdown lists all 12 languages. Picking one is used even if auto-detect disagrees. |
| F3 | Show the text in the speaker's own language, and let the user edit it | Must | Caller, Reviewer | Speech errors on Indian languages are large (H5, H6, S7, S8), so a person needs a way to fix a wrong word | Editing the text and re-running changes the English text and the prediction |
| F4 | Translate to English and show it read-only, labelled "machine translation" | Must | Reviewer, Evaluator | The classifier only understands English (Phase 3 decision). Both texts are shown so a person can check the step (H4, S5). | English text appears within the time target. IFSC, UPI, PIN and OTP survive on the sample clips. |
| F5 | Show the intent class number (0 to 13) and its name | Must | Reviewer, Evaluator | The project document asks for a prediction (step 19). Names come from intent_info.csv. | Number and name are shown on the check screen |
| F6 | Show a confidence percentage and the list of checks that passed or failed | Must | Reviewer, Evaluator | The project document asks for a confidence score (step 20). The plan combines four checks. | Percentage is the highest predict_proba value. Failed checks are listed by name. |
| F7 | Show the lane (self-serve, guided action, urgent, sales lead, human review) | Must | Reviewer | Lanes are the plan's way to turn a prediction into a safe decision. Urgent calls matter most (H3, S1, S2). | Lane appears on the check screen and in the log |
| F8 | Read-back sentence in the caller's language, with Yes, No (record again) and Talk to a person buttons | Must | Caller | "Confirm before acting" is a design principle from Phase 1. A wrong urgent call is costly, a read-back is cheap. | Buttons work and the choice is logged |
| F9 | Correction loop: re-run from edited text, and log both the machine text and the corrected text | Should | Reviewer | Corrections are the best future training data (plan) | Both versions appear in the event log |
| F10 | Reviewer queue: low-confidence clips with both texts, the top two guesses, an override dropdown, a resolve button, and a CSV export | Should | Reviewer | Human in the loop (plan, and "People First" in S5). H4 is only partly supported. | A clip can be overridden and resolved, and the export opens in Excel |
| F11 | Event log in logs/events.csv, text only, no audio | Must | Evaluator, Reviewer | Every step must be checkable (plan). Customer text may be private, so no audio. | One row is written per clip with the fields in section 6 |
| F12 | Demo mode: one click plays a clip from data/sample_audio/ and runs the whole pipeline | Must | Evaluator | Evaluators may not have a microphone (plan) | Every clip in the manifest runs with one click |
| F13 | Plain-words error messages that always offer "Talk to a person" | Must | Caller | Never trap the caller (Phase 1). The six messages are in wireframes.md. | Each of the six situations shows its message |
| F14 | Thumbs-up or thumbs-down gesture to answer the read-back, using the webcam | Could | Evaluator | The project document lists MediaPipe as optional (step 21) and says a simple version is enough | Only built after F1 to F13 work |
| F15 | On-screen privacy notice: your voice is not saved, the text may be sent to an online translator, and please do not say real card, account or phone numbers | Must | Caller, Evaluator | The online translator sends text over the internet (plan, Phase 0). The log stores text, so real numbers would end up in the log and with the translator (risk R20). | Notice visible on the caller screen |
| F16 | Check screen: one screen that shows every field (language, original text, English text, class number and name, confidence, lane, checks, time per step) | Must | Evaluator, Reviewer | This is the project document's final expected output (section 23) | All fields shown for one clip |
| F17 | After the caller taps Yes, show a simulated next step for the lane (for example "In a real system, a person would now help you block your card"). No real bank action. | Must | Caller, Evaluator | Found in review: the PRD says the prototype takes no bank action, but a "self-serve answer" would need a bank system. Without this the demo ends with nothing happening. | Each of the 5 lanes shows its own message (texts are in the wireframes update) |

Read-back rule: the read-back (F8) is shown for every clip that reaches an automatic lane. In the urgent lane the caller cannot skip it, and after Yes the call goes to a person.

### 2.2 The three screens

The wireframes are in wireframes.md.

| Screen | Contains | Features |
| --- | --- | --- |
| Caller screen | Record, language, what I heard, what you want, how sure (High, Medium, Low), read-back buttons, privacy notice | F1, F2, F3, F8, F13, F15 |
| Check screen | Every field, with numbers | F3 to F7, F9, F16 |
| Reviewer queue | Clips sent to a person, with top two guesses and override | F10 |

The caller screen deliberately hides the class number and the lane. A class number means nothing to a caller, and the word "URGENT" could frighten them (Phase 1 mock-up review).

### 2.3 The four checks

The PRD mentions "checks" in F6 and F7 but never defined them. Here they are. The cut-off numbers are set in Phase 7 from a threshold sweep, not guessed now.

| Check | Passes when | Comes from | Numbers set in |
| --- | --- | --- | --- |
| Language check | The user chose the language, or the auto-detect score is high | Dropdown, stt.py | Phase 7 |
| Speech check | The speech engine's reliability signals look fine, and the clip is not too quiet or too short | stt.py | Phase 7 |
| Translation check | The translation did not time out, and the English text has at least one banking word (not needed for English clips) | translate.py | Phase 7 |
| Classifier check | The highest probability is at or above the threshold of its lane | The saved model | Phase 7 |

Rule: a clip goes to an automatic lane only if all four checks pass. If any fails, it goes to human review.

"How sure: High, Medium or Low" on the caller screen is a plain-words version of the classifier probability. The cut-offs for High, Medium and Low are decided in Phase 7.

## 3. Who it is for

| User | What they do | What they need | Basis |
| --- | --- | --- | --- |
| Caller | Speaks one request and confirms it | Short prompts, their own language, a way to fix mistakes, a person always available | Persona 1, with assumptions marked (personas_and_journeys.md) |
| Reviewer | Checks clips the machine is unsure about | Both texts, the top two guesses, the override | Persona 2, H4 (partly supported) |
| Evaluator | Looks at the project (instructor, recruiter) | A demo that works without a microphone, and visible numbers | Project document |

## 4. What success looks like

Targets come from targets_and_languages.md (Phase 1). "Commit" is what I will be held to.

### 4.1 Quality

What "correct in the self-serve lane" means: of the calls the system sends automatically to the self-serve lane, at least 95% have the right intent. Calls sent to a person are not counted here. They are counted in the "share sent to a person" number.

| Measure | Core languages | Experimental languages | Basis |
| --- | --- | --- | --- |
| Correct in the self-serve lane | At least 95% | Measure and publish, no pass mark | Plan |
| Urgent intents (classes 8, 12, 13) | Report as counts, for example "14 of 15", with no misses on typed text | Measure and publish | Test sets are too small for a percentage (targets file) |
| Share of calls sent to a person | At most 40% (stretch: under 25%) | Measure and publish | Published containment examples run from 40% to 77% (S11) |

### 4.2 Speed (targets, not measurements)

| Step | Target | Basis |
| --- | --- | --- |
| Speech to text, clip of about 5 s | Up to 5 s | **Measured:** Whisper base took 1.1 s on a short English clip (HP OMEN 16, Phase 0). Larger models for Indian languages (Phase 4 gate) are slower and not measured yet. |
| Translation | Up to 2 s (target). Measured: 3.76 s average over 10 calls with MyMemory, because Google was blocked. | **Measured 18 Nov (HP OMEN 16):** 10 of 10 calls were over 2 s. A rerun with the skip rule is in phase5_results.md. English clips skip translation, so they take 0 s. |
| Preprocessing, vectorizer, model and router | Up to 0.5 s | Assumption. The toy model in the smoke test took 0.014 s, but the real model is bigger, so I left room. |
| Total, for a clip of up to 10 s | Up to 8 s for English. Hindi is about 9 s and Marathi is longer. | English: about 1 s speech plus 0 s translation plus 0.5 s. Hindi: 4.85 s plus 3.76 s plus 0.5 s. Marathi: 8.8 s plus 3.6 s plus 0.5 s. The screen shows a progress message for any step over 2 s. |

### 4.3 Project-level

| Measure | Target |
| --- | --- |
| Someone who has never seen the app can record in two languages and explain the result | Yes (plan, Phase 8 done-when) |
| Demo mode runs for every clip in the manifest | 100% |
| Every demo language has a status (core or experimental) backed by numbers | Yes (Phase 9) |

## 5. Scope

### 5.1 In scope for version 1

- The 12 languages from the plan: English, Hindi, Marathi, Tamil, Telugu, Kannada, Bengali, Urdu, Manipuri (Meitei), Rajasthani, Spanish, Russian.
- One short clip at a time, recorded in the browser or uploaded.
- The 14 intents from intent_info.csv.
- Runs locally on a laptop CPU.

### 5.2 Out of scope for version 1

| Item | Reason |
| --- | --- |
| Real telephony (an actual phone line) | The plan excludes it. Skit-S2I was recorded over a phone line at 8 kHz (S6), but we only use browser audio. |
| Login, authentication and bank integration | The plan excludes them. The prototype takes no bank action. |
| Mixed-language speech such as Hinglish | The plan excludes it. It is logged as an example if it happens. |
| Separating two speakers on one call | The plan excludes it |
| Voice yes or no answers | Buttons only in version 1 (plan) |
| Giving advice on fraud-reporting rules | The RBI window is changing (S1, S2), so the machine does not quote it. A person does. |
| More than the 12 languages | Scope creep (risk list) |
| Security of the Caller and Reviewer mode switch | The switch is for the demo only, and anyone can flip it. Real access control needs a login, which is out of scope. |

## 6. Non-functional requirements

| Need | Requirement | Reason |
| --- | --- | --- |
| Clip length | At least 1 second, at most 15 seconds | Skit clips run from 1.5 to 8.19 seconds, average 4.2 seconds (S6). Changed from the plan's 30 seconds. |
| Audio storage | None by default. A hash of the clip may be logged, never the audio. | Plan. Callers may say private things. |
| Log fields | Time, language chosen and detected, audio hash, original text, English text, class number, label, confidence, failed checks, lane, final label, whether corrected, time per step | Plan. One row per clip, text only. |
| Log location | logs/events.csv, kept out of Git | The .gitignore from Phase 0 excludes logs/ |
| Scripts | Every script displays correctly. Urdu runs right to left. Meitei Mayek needs a font that supports it. | Plan. Tested with script_test.html. |
| Failures | A plain message in every failure case, and "Talk to a person" is always offered | Phase 1 principle |
| Translator reliability | A timeout and a fallback translator | **This already happened in Phase 0:** Google returned "too many requests" |
| Translator privacy | If an online translator is used, the screen and the README say that the text leaves the machine, and an offline option stays available | Plan |
| Platform | Windows laptop, CPU only, Python 3.11.9. Reference machine for every timing: HP OMEN 16, 24 GB RAM, Intel Core Ultra 7 255H. | Phase 0 smoke test. Timings on another machine will differ. |
| Translator timeout | Each translation call stops after 5 seconds and the next translator is tried | Google was blocked in Phase 0. MyMemory took 1.84 s, so 5 s is about 2.7 times the typical time. With speech at 1.1 s the total stays near 7 s (1.1 + 5 + 0.5). |
| What callers say | The screen asks callers not to say real card, account or phone numbers | The log stores text, and text may go to an online translator (risk R20) |
| Browser | Latest Chrome (an assumption about what will be tested) | Not decided by evidence |
| Reproducibility | Seed 42 everywhere, versions pinned with pip freeze at the end | Plan |
| Licence | Non-commercial research use only | Skit-S2I is CC BY-NC 4.0 (S6) |

## 7. Plain-language labels for the 14 intents

These are the words the caller screen shows after "I think you want:". They are my draft English wording based on intent_info.csv. Read-back sentences and their translations are finished in Phase 7, and a native speaker must check the translations.

| Class | Name in intent_info.csv | Caller screen wording |
| --- | --- | --- |
| 0 | branch_address | Find a branch address |
| 1 | activate_card | Activate your card |
| 2 | past_transactions | See your past transactions |
| 3 | dispatch_status | Check the delivery of your card |
| 4 | outstanding_balance | Check the amount due on your card |
| 5 | card_issue | Report a problem using your card |
| 6 | ifsc_code | Get a branch IFSC code |
| 7 | generate_pin | Set or change your PIN |
| 8 | unauthorised_transaction | Report a transaction you did not make |
| 9 | loan_query | Ask about a loan |
| 10 | balance_enquiry | Check your account balance |
| 11 | change_limit | Change your card limit |
| 12 | block | Block a card or banking product |
| 13 | lost | Report a lost card |

## 8. How this matches the project document

| Project document section | What the PRD does about it |
| --- | --- |
| 16 Load the saved model | The app loads best_model.pkl and vectorizer.pkl once and caches them |
| 17 Streamlit UI | F1, F16 |
| 18 Speech-to-text | F1, F2, F3 |
| 19 Prediction, using the same preprocessing as training | F5. preprocess.py is shared by the notebook and the app. |
| 20 Confidence score | F6 |
| 21 MediaPipe gestures (optional) | F14, a Could item |
| 22 Final project structure | The file map from the plan |
| 23 Final expected output | F16, the check screen |

## 9. Assumptions and open questions

| # | Assumption or question | How it will be settled |
| --- | --- | --- |
| A1 | Callers prefer their own language on the phone | Only indirect evidence (H1). Not testable without real people. |
| A2 | Simple lookups are a large share of calls | Weak, old and mostly US evidence (H2) |
| A3 | Whisper base is good enough for English | Test in Phase 0 passed on one English clip. Test more in Phase 4. |
| A4 | A larger model is needed for Marathi, Tamil, Telugu and maybe Hindi | The Phase 4 gate |
| A5 | The translation step stays under 2 seconds | **Not true on this network.** Measured 3.76 s average (MyMemory, Google blocked). Re-measured after the skip rule, see phase5_results.md. |
| A6 | The RBI fraud-reporting window and its start date | Check rbi.org.in before quoting. The app does not quote it. |
| A7 | The cut-offs for "High, Medium, Low" on the caller screen | Decided in Phase 7 from the threshold sweep |
| A8 | A caller can read the English line on the screen | Not true for a Marathi-only caller. The line is relabelled "For staff" (see the wireframes update). |
| A9 | MyMemory's free daily limit | I recall there is a limit for anonymous use, but I did not verify it. Check before any demo. |

| Q1 | Does a native speaker find the draft sentences and error messages natural? | Phase 4 and Phase 7 |

## 10. Change log

| Date | Change | Reason |
| --- | --- | --- |
| 17 Nov 2026 | Maximum clip length 15 seconds instead of 30 | Skit clips are at most 8.19 seconds (S6) |
| 17 Nov 2026 | Translator fallback and timeout made a requirement | Google blocked the Phase 0 test |
| 17 Nov 2026 | Added F16, the check screen | It is the project document's expected output, and the caller screen hides most fields |
| 17 Nov 2026 | App must not quote fraud-reporting windows | RBI rules are changing (S1, S2) |
| 17 Nov 2026 | Translation measured at 1.84 s (MyMemory). Added a 5 s translator timeout. Added the reference machine. | Phase 0 results |
| 17 Nov 2026 | F15 expanded. F17 (simulated next step) added. Section 2.3 (the four checks) added. | AI review of the PRD |
| 17 Nov 2026 | "Correct in the self-serve lane" defined. Read-back rule made single. | AI review of the PRD |
| 18 Nov 2026 | Translation speed target kept at 2 s, but the measured value (3.76 s) is written next to it. Hindi and Marathi totals are over 8 s. | Phase 5 timing results |
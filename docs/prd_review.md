# PRD review

## A. Status

| Item | Status |
| --- | --- |
| Review by a second person | Done by Claude (an AI assistant), **not a human**, on 17 November 2026 |
| Was the reviewer a blind reader? | No. The same assistant wrote the first version of the PRD in an earlier chat. This was a critical second read, not a stranger test. |
| Review by a human | Not done. Optional 2 minute route in section D. |
| Self-check by the author | Done on 17 November 2026 (section B of the first version, kept below in section C) |

## B. Review answers (the kit's three questions)

Reviewer: Claude (AI assistant)
Date: 17 November 2026

1. **In one sentence, what does the app do?**
   It takes one short voice clip in one of 12 languages, shows what it heard and an English translation, guesses which of 14 banking requests it is, says how sure it is, and sends unsure or urgent calls to a person.
2. **Did it match the PRD summary?** Yes. With the caveat that I am not a blind reader.
3. **What was unclear or missing?** Nine things, listed below.
4. **Caller-screen concerns:** two, listed below.

### Gaps found

| # | Gap | Why it matters | Fix |
| --- | --- | --- | --- |
| 1 | After the caller taps Yes, nothing is defined. "Self-serve answer" would need a bank system, which is out of scope. | The demo would end with nothing happening | Added F17 and five simulated messages |
| 2 | Read-back rule disagreed between Phase 1 (urgent only) and F8 (every clip) | Two rules for one behaviour | One rule: every automatic lane, and urgent cannot skip it |
| 3 | "How sure: High, Medium, Low" had no definition | Nobody could build or test it | Cut-offs set in Phase 7 (A7) |
| 4 | "Four checks" were mentioned but never listed | F6 and F7 could not be built | Added Section 2.3 |
| 5 | "95% correct in self-serve" did not say what it is 95% of | It could be read two ways | Defined in Section 4.1 |
| 6 | The Caller and Reviewer mode switch looks like security | A reader may think access is protected | Added to out of scope |
| 7 | Callers may say real card or account numbers into the demo | They would land in the log and with the online translator | Added to F15, Section 6 and risk R20 |
| 8 | Translation speed was "not measured" | The speed table was out of date | Updated with 1.84 s and a 5 s timeout |
| 9 | The reference machine was not named | Timings mean nothing without it | Added to Section 6 |

### Caller-screen concerns

1. The English line is shown to a caller who may not read English. Fix: relabelled "For staff".
2. "Talk to a person" must also exist in the caller's own language, not only in English. Fix: added to the Phase 7 list of sentences a native speaker checks.

### What I could not judge

- Whether a real caller finds the wording natural. Only a native speaker or a real caller can say.
- Whether the numbers in the targets are right. They are design choices with reasons, not measurements.

## C. Self-check from the first version (kept for the record)

| # | Question | Answer from the PRD | Where |
| --- | --- | --- | --- |
| 1 | What does the app do? | Listens to one short clip in one of 12 languages, shows the text in the speaker's language and in English, predicts one of 14 banking intents, shows confidence and a lane | Section 1 |
| 2 | Who uses it? | A caller, a reviewer and an evaluator | Section 3 |
| 3 | What does it not do? | No real phone line, no login, no bank actions, no mixed-language speech, no fraud-window advice | Section 5.2 |
| 4 | What does success look like? | At least 95% correct in self-serve for core languages, urgent intents reported as counts, at most 40% sent to a person, speed targets, a demo that works | Section 4 |
| 5 | Which features are essential? | F1 to F8, F11 to F13, F15, F16 and F17 are Must | Section 2.1 |
| 6 | How fast should it be? | Up to 8 seconds in total for a clip of up to 10 seconds | Section 4.2 |
| 7 | What does it store? | Text and a hash in logs/events.csv. No audio. | Section 6 |
| 8 | What is unproven? | Whether callers prefer their own language on the phone, the call mix, translation speed over many calls, and whether larger models fix Indian languages | Section 9 |

## D. If your instructor wants a human reviewer (2 minutes of your time)

You do not have to explain anything. Send PRD.md, wireframes.md and the message below to one classmate or senior. When they reply, paste their three answers under "Human review" at the bottom of this file.

```
Hi [name], I am building a college project for a voice system that understands
what a caller wants when they speak to a bank in their own language. Could you
read the attached two files for about 10 minutes and answer three questions?
1. In one sentence, what does the app do?
2. What is the one thing that is unclear or missing?
3. Is anything on the caller screen confusing or worrying?
Please be blunt.
```

## Human review

Reviewer: (not done yet)
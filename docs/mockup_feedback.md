# Mock-up feedback

Status of feedback from real users: none collected yet.

What this file contains instead: (A) my own review of the mock-up against ten standard usability heuristics (Jakob Nielsen's list, from my own knowledge, not looked up today), (B) the improved mock-up, and (C) the questions still to ask real people.

## A. Heuristic review of mock-up version 1

This is a review by the builder, not by users. It finds likely problems, but it cannot show what users actually do.

Mock-up version 1 (from the plan):

```
[ Record ]   Language: Auto-detect: Hindi (xx%)   [change]
Audio:       play  0:03
Original:    (text in the caller's language)   (editable)
English:     My card is lost
Class:       13      Label: lost
Confidence:  xx%     Lane: URGENT
Read-back:   You want to report a lost card. Is that right?
             [ Yes ]   [ No, record again ]   [ Talk to a person ]
```

| # | Heuristic | What I found in version 1 | Change in version 2 |
| --- | --- | --- | --- |
| 1 | Show what the system is doing | "xx%" gives no meaning to a caller | The caller sees "How sure: High, Medium or Low". The reviewer sees the percentage. |
| 2 | Match the real world | "Class: 13, Label: lost" is jargon for a caller | The caller sees "Report a lost card". Class number and label are shown only on the reviewer screen. |
| 3 | User control | Yes, No and Talk to a person are there, which is good | "Talk to a person" is also shown on every error message |
| 4 | Consistency | The word "Lane: URGENT" might frighten a caller | Lane is hidden on the caller screen and shown only to the reviewer |
| 5 | Prevent errors | Read-back before acting is good | Kept for urgent classes (8, 12, 13) |
| 6 | Recognise, don't recall | The original text is editable, which is good | The English text is shown read-only, with a note that it is a machine translation |
| 7 | Flexibility | Auto-detect might pick Urdu instead of Hindi | The language dropdown is always shown and always wins over auto-detect |
| 8 | Minimal design | Too many fields for a stressed caller | The caller screen has 4 things: what I heard, what you want, and 3 buttons |
| 9 | Help with errors | No error screens were drawn | Six error messages written below |
| 10 | Privacy and trust | Nothing says the audio is not stored | A one-line notice: "Your voice is not saved." (the plan stores no audio by default) |

Also checked: Urdu runs right to left, so the original-text box needs a right-to-left rule. Meitei Mayek needs a font that supports it (the plan already says this). Both are Phase 8 tasks.

## B. Mock-up version 2

Caller screen:

```
[ Record ]   Language: Marathi   [change]
Play:        > 0:03
I heard (you can fix it):   (text in the caller's language)
In English (machine translation):   My card is lost
I think you want:   Report a lost card
How sure:   High
Is that right?   [ Yes ]   [ No, record again ]   [ Talk to a person ]
Your voice is not saved.
```

Reviewer screen:

```
Clip: 0003   Language: Marathi (chosen)   Language score: xx%
Original:   (text, editable)
English:    My card is lost
Top guess:   13 lost       Confidence: xx%     Lane: Urgent
Second guess:   5 card_issue     Confidence: xx%
Checks:   language ok | speech ok | translation ok
Override:   [ dropdown of the 14 class names ]   [ Resolve ]
```

Error messages (English wording; translations need a native speaker later):

| Situation | Message |
| --- | --- |
| Silence or too quiet | "I could not hear you. Please try again, closer to the phone." |
| Too short | "That was very short. Please say a full sentence." |
| Unsupported language | "I cannot understand this language yet. Let me connect you to a person." |
| Low language score | "Did you speak Hindi or Urdu? Please choose." (only for confusable pairs) |
| Translation failed or timed out | "I am having trouble. Let me connect you to a person." |
| Anything unexpected | "Something went wrong. Let me connect you to a person." |

## C. Questions to ask real people later (not asked yet)

| # | Question | Status |
| --- | --- | --- |
| M1 | Would you trust this label? | Not asked |
| M2 | Does the original text look right to you? (native speakers only) | Not asked |
| M3 | Would you feel safe using this? | Not asked |
| M4 | What is the first thing you looked at on the screen? | Not asked |
| M5 | Is anything missing, or anything you do not understand? | Not asked |

Optional 10-question form (only worth sending if 30 or more people will answer; report it as a small sample if you do):

1. In which language do you prefer to talk to your bank on the phone?
2. Have you ever had trouble using a bank's phone menu? (Yes, No, Never called)
3. If yes, what went wrong?
4. Would you speak your problem to a machine instead of pressing buttons? (Yes, Maybe, No)
5. What would make you trust it more?
6. Look at the screen picture. What does "I think you want: Report a lost card" tell you?
7. Would you tap "Yes" on it? (Yes, Not sure, No)
8. What is missing from the screen?
9. How comfortable are you if a machine writes down what you said? (1 to 5)
10. Anything else?
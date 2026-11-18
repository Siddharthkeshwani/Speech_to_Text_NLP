# Personas and journeys

Both personas are fictional composites. I made them up to guide design. No real person is described here. Every detail is tagged either with a source ID from research_sources.md or with "Assumption".

## Persona 1: the caller (fictional)

| Detail | Value | Where it comes from |
| --- | --- | --- |
| Name | Sunita | Made up |
| Language | Marathi | Marathi is the third-largest mother tongue, 6.86% of the population (S3). It is also the language in the plan's own example. |
| Comfort with technology | Low to medium | Assumption. The closest evidence is that 41% of people are offline and some of them cite missing local-language content (S4). That is about a group, not about her. |
| Stress when calling | High | Reasoned from S1 and S2: the customer's protection depends on how fast a fraud is reported, so a lost card is a pressured call. This is my reasoning, not a measurement. |
| What she wants | To tell the bank in Marathi and be sure it understood | Assumption (H1, partly supported) |
| What she fears | Pressing the wrong menu button, or speaking and not being understood | Assumption |

## Persona 2: the reviewer (fictional)

| Detail | Value | Where it comes from |
| --- | --- | --- |
| Name | Rahul | Made up |
| Role | Contact-centre supervisor who checks the clips the machine is unsure about | Assumption. This role is in the plan. |
| What he needs | The original text, the English text, the guessed intent, the score and the top two guesses on one screen, and a quick way to correct them | Direction from S5 (explainability, humans in the loop). The specific list is my design, and H4 is only partly supported. |
| What he fears | A wrong label that sends an urgent call to the wrong place | Assumption, linked to H3 |
| How long he has per clip | Not set | I found no number. Do not invent one. |

## Journey 1: lost card, in Marathi

| Step | What happens | System part | Why |
| --- | --- | --- | --- |
| 1 | Sunita presses Record and says in Marathi that her card is lost | Recorder | A short prompt is easier when stressed |
| 2 | The screen shows the Marathi text she said, and she can edit it | stt.py | She must be able to fix a wrong word (H5) |
| 3 | The screen shows the English translation | translate.py | Staff can check it too |
| 4 | The system guesses the intent: lost card (class 13) | Classifier | From intent_info.csv |
| 5 | All checks pass and the confidence is high, so it goes to the Urgent lane | router.py | Urgent calls should reach a person fast (S1, S2) |
| 6 | The system asks in Marathi: "You want to report a lost card. Is that right?" | Read-back | Confirm before acting |
| 7 | She taps Yes | App | |
| 8 | The call goes to a person to block the card | Handoff | The machine does not block cards in version one |
| 9 | If any step fails or she taps "Talk to a person", she goes to a person at once | Router | Never trap the caller |

## Journey 2: a low-confidence clip

| Step | What happens | System part | Why |
| --- | --- | --- | --- |
| 1 | A clip arrives with background noise and a low language score | stt.py | Whisper's language detection can be unsure on short or noisy clips (assumption) |
| 2 | The system does not guess. It puts the clip in the reviewer queue | router.py | A wrong guess costs more than a human look |
| 3 | Rahul sees the audio, original text, English text and the top two guesses | Reviewer tab | H4 (untested) |
| 4 | He picks the right intent from a dropdown and presses resolve | Reviewer tab | |
| 5 | Both the machine text and his correction are saved | logger.py | Corrections are useful training data later |

## Journey 3: unauthorised transaction, in Hindi

| Step | What happens | System part | Why |
| --- | --- | --- | --- |
| 1 | A caller says in Hindi that money was taken from the account without permission | Recorder and stt.py | |
| 2 | The system guesses class 8 (unauthorised transaction) | Classifier | |
| 3 | Fraud always goes to a person at once, with no automatic answer | router.py | The plan's rule. Also S1 says the bank must act immediately on a report. |
| 4 | The person, not the machine, tells the caller about the reporting window and the 1930 helpline | Human agent | The window is changing (S1, S2), so the machine should not quote it |

## Design principles, with reasons

| Principle | Reason |
| --- | --- |
| Short prompts | The caller may be stressed, and it is voice only |
| Confirm before acting | Wrong intents on urgent calls are costly, and a read-back is cheap |
| Never trap the caller | "Talk to a person" is on every screen, including error screens. This also fits "People First" in S5. |
| Show the evidence | The reviewer sees both texts and the score. This fits "Understandable by Design" in S5. |
| Say the limits | If a language is not supported, the app says so and offers a person. The plan states that "any language" is not achievable. |
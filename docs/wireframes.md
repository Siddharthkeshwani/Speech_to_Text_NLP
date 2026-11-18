# Wireframes

Black and white, structure only, no colour (as the plan says). Version 2, 17 November 2026, built from the heuristic review in mockup_feedback.md.

The sketches use real text in several scripts. The sentences are my own wording and have NOT been checked by a native speaker. They are only for testing the layout.

## Screen flow

```
Caller screen  --Yes-->  Done (hand-off or answer)
     |
     +--No, record again--> Caller screen
     |
     +--Talk to a person--> Hand-off to a person
     |
     +--Low confidence or failed check--> Reviewer queue

Check screen = the same clip with every field and number shown.
It is opened from a tab, and it is what an evaluator looks at.
```

## Wireframe 1: Caller screen (Marathi example)

```
+----------------------------------------------------------+
| Speak your request                                       |
|                                                          |
| Language: [ Marathi v ]   (always overrides auto-detect) |
|                                                          |
|   [ ( ) Record ]      [ Upload a file ]                  |
|                                                          |
| Play:  [ > ]  0:03                                       |
|                                                          |
| I heard (you can fix it):                                |
| +------------------------------------------------------+ |
| | माझे कार्ड हरवले आहे                                   | |
| +------------------------------------------------------+ |
|                                                          |
| For staff (English, machine translation):                |
|   My card is lost                                        |
|                                                          |
| I think you want:  Report a lost card                    |
| How sure:          High                                  |
|                                                          |
| Is that right?                                           |
|  [ Yes ]   [ No, record again ]   [ Talk to a person ]   |
|                                                          |
| Your voice is not saved. The text may be sent to an      |
| online translator. Please do not say real card, account  |
| or phone numbers.                                        |
+----------------------------------------------------------+
```

### States of the caller screen

| State | What the screen shows |
| --- | --- |
| Start | Only the language box and the Record and Upload buttons |
| Recording | "Listening..." and a Stop button |
| Working | "Reading your message..." and which step is running (speech, translation, intent) |
| Result | The full screen above |
| Error | One of the six messages below, with the Talk to a person button |

### Error messages (English wording; translations need a native speaker later)

| Situation | Message |
| --- | --- |
| Silence or too quiet | "I could not hear you. Please try again, closer to the phone." |
| Too short (under 1 second) | "That was very short. Please say a full sentence." |
| Too long (over 15 seconds) | "That was long. Please say it in one or two sentences." |
| Unsupported language | "I cannot understand this language yet. Let me connect you to a person." |
| Low language score on a confusable pair | "Did you speak Hindi or Urdu? Please choose." |
| Translation failed or timed out, or anything unexpected | "I am having trouble. Let me connect you to a person." |

### What the screen shows after the caller taps Yes (simulated, no real bank action)

| Lane | Message on screen |
| --- | --- |
| Self-serve | "In a real system, your answer would be read to you now. (Demo: no bank connection.)" |
| Guided action | "In a real system, we would help you with this after a security check. (Demo: nothing is changed.)" |
| Urgent | "A person will help you now. In a real system your call would be handed over immediately." |
| Sales lead | "A loan advisor would call you back. (Demo: nothing is sent.)" |
| Human review | "A person will check your request. (Demo: it is now in the reviewer queue.)" |

These are my English wording. A native speaker checks the translations in Phase 7.

## Wireframe 1b: Caller screen in Urdu (right to left)

```
+----------------------------------------------------------+
|                                         Speak your request|
|                                                           |
|            ( always overrides auto-detect )  [ Urdu v ]   |
|                                                           |
|                      [ Upload a file ]      [ ( ) Record ]|
|                                                           |
|                                              0:03  [ > ]  |
|                                                           |
|                                   :(you can fix it) I heard|
| +------------------------------------------------------+ |
| |                                  میرا کارڈ کھو گیا ہے   | |
| +------------------------------------------------------+ |
|                                                           |
| English text and the buttons stay left to right.          |
+----------------------------------------------------------+
```

What this sketch is for: only the box with the Urdu text must be right to left (the text aligns to the right, and the cursor starts on the right). The labels and buttons can stay left to right, which is simpler to build. The sketch shows the fully mirrored look so the choice is visible. Decision: **mirror only the text box in version 1**, because mirroring the whole page in Streamlit takes extra work (my judgement, not tested).

## Wireframe 2: Check screen

```
====================================================
  Multilingual Speech-to-Text Intent Prediction
====================================================
Language:       Marathi (chosen)     Detection score: not used
Audio:          [ > ] 0:03           (not saved)

Original text:  माझे कार्ड हरवले आहे            [ edit ]
English text:   My card is lost

Prediction:     Class 13 - lost
Confidence:     xx%
Lane:           Urgent
Checks:         language ok | speech ok | translation ok

Top two:        1) 13 lost       xx%
                2) 5  card_issue xx%

Time:           speech x.x s | translation x.x s | classifier x.x s

Gesture:        (optional) thumbs-up detected
====================================================
```

Notes:

- This follows the project document's expected output (section 23): recognized text, prediction, confidence, gesture.
- The "xx" and "x.x" are placeholders. Real numbers appear only after the model and the timing code exist.
- "Language: Marathi (chosen)" is replaced by "Hindi (auto-detected, xx%)" when the dropdown is on Auto-detect.

## Wireframe 3: Reviewer queue

```
Reviewer queue          Mode: [ Reviewer v ]       [ Export CSV ]

+----+-------+---------------------+--------------+-----------+-----------+------------------+
| #  | Lang  | Original (short)    | English      | Top guess | 2nd guess | Why it is here   |
+----+-------+---------------------+--------------+-----------+-----------+------------------+
| 1  | Hindi | मेरा कार्ड खो गया है  | My card is   | 13 lost   | 5 card_   | Low language     |
|    |       |                     | lost         | xx%       | issue xx% | score            |
+----+-------+---------------------+--------------+-----------+-----------+------------------+
| 2  | Urdu  | میرا کارڈ کھو گیا ہے  | (translation | not run   | not run   | Translation      |
|    |       |                     |  timed out)  |           |           | timed out        |
+----+-------+---------------------+--------------+-----------+-----------+------------------+
| 3  | Tamil | என் கார்டு தொலைந்துவிட்டது | My card is  | 13 lost   | 12 block  | Experimental     |
|    |       |                     | lost         | xx%       | xx%       | language         |
+----+-------+---------------------+--------------+-----------+-----------+------------------+

Selected clip: #1
  Audio [ > ]    Original (editable): मेरा कार्ड खो गया है
  English: My card is lost
  Override: [ 13 lost v ]   [ Resolve ]
```

Notes:

- Row 2 shows the right-to-left cell in a left-to-right table. The Urdu text should align to the right inside its own cell.
- The "Why it is here" column is the failed check or the rule that sent the clip to a person. It is what makes the label checkable (H4, S5).
- The override dropdown lists the 14 class names, not just numbers.

## Layout problems spotted early

| # | Problem | What to do | When |
| --- | --- | --- | --- |
| 1 | Urdu runs right to left, but the rest of the page runs left to right | Mirror only the text box (decision above) | Phase 8 |
| 2 | Tamil, Telugu and Kannada words are long and wrap badly in narrow table cells | Give the original-text column more width and allow wrapping | Phase 8 |
| 3 | Meitei Mayek needs a font that supports it, and many computers do not have one | Use the Bengali-script option for Manipuri if the font will not show, or load a Noto font. Run script_test.html first. | Phase 8 |
| 4 | Rajasthani uses the same script as Hindi, so the screen cannot tell them apart | The dropdown is the only way to choose it. Label it experimental. | Phase 8 |
| 5 | A long Marathi or Hindi sentence in the editable box can push the buttons down | Give the box a fixed height with scrolling | Phase 8 |
| 6 | The class number means nothing to a caller | Show it only on the check screen and in the reviewer queue | Done in version 2 |

## Streamlit mapping (a hint for Phase 8)

| Part of the wireframe | Streamlit idea |
| --- | --- |
| Language dropdown, mode switch, demo switch | The sidebar |
| Caller screen, check screen, reviewer queue | Three tabs on one page |
| Editable original text | A text area |
| Yes, No and Talk to a person | Three buttons |
| Reviewer table | A table or data editor |

I have not built any of this yet. It is only a plan for Phase 8.


## Script test result (script_test.html opened in Chrome, 17 November 2026)

| Language | Shows properly? | Note |
| --- | --- | --- |
| English | Yes | |
| Hindi | Yes | |
| Marathi | Yes | |
| Tamil | Yes | Wrapped onto two lines in the table cell |
| Telugu | Yes | Readable |
| Kannada | Yes | Readable |
| Bengali | Yes | Readable |
| Urdu | Yes | Aligned to the right as intended. Looks smaller than the other rows. |
| Manipuri (Meitei Mayek) | Letter shapes appear, not empty boxes | Font test only. I cannot check each letter from a screenshot. |
| Rajasthani | Yes | Same Devanagari text as Hindi |
| Spanish | Yes | |
| Russian | Yes | |

What this changes:

1. Layout problem 2 (long Tamil words wrap) is confirmed. Give the original-text column more width.
2. Layout problem 3 (Meitei Mayek font) is not a problem on this machine, so the Bengali-script backup is not needed here. Another computer may lack the font, so keep the Noto font fix in mind for the demo machine.
3. New: the Urdu text looks smaller than the other scripts. Give the Urdu text box a slightly bigger font size in Phase 8.
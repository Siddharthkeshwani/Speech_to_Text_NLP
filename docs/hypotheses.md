# Hypotheses

Status rule (my own, written before I judged them):

| Status | When I used it |
| --- | --- |
| Supported | At least one grade A or B source says it directly (grades are in research_sources.md) |
| Partly supported | Sources point the same way, but they are indirect, old, from another country, or from vendors |
| Not testable by desk research | Only a real person can answer it |

Important: nothing here comes from interviews. "Supported" means "published evidence agrees", not "a banker told me".

## Summary

| # | Hypothesis | Status |
| --- | --- | --- |
| H1 | Callers want to speak in their own language, and many cannot use menus in English or Hindi | Partly supported |
| H2 | Simple intents (balance, IFSC code, branch location, card status) are a large share of calls | Partly supported |
| H3 | Lost-card, block and fraud calls are time-critical | Supported |
| H4 | Staff will trust a label only if they can see the original text, the English text and a score | Partly supported |
| H5 | Translation and speech errors are a bigger risk than classification errors | Partly supported (speech part strongly) |
| H6 (added after research) | Whisper `base` is too weak for Indian languages, so Phase 4 needs a stronger speech model or a decision gate | Supported |

## H1: Callers want their own language

- Evidence for:
  - 57% of urban internet users prefer to use the internet in Indic languages (S4).
  - 13% of the people who are offline say lack of local-language content is a reason (S4).
  - Only about 2.6 lakh people in the 2011 Census report English as their mother tongue, and the largest mother tongue is Hindi at 43.63% (S3, S3b).
- Evidence missing: nothing I found is about phone banking or IVR menus. The sources are about internet content.
- Why "Partly supported" and not "Supported": the leap from "prefers Indic content online" to "cannot use an English or Hindi IVR menu" is my assumption. I did not find a source that says it directly.
- What a real person could add: how callers in regional languages are handled today, and what happens when they cannot find a menu option.

## H2: Simple intents are a large share of calls

- Evidence for:
  - Over half of US bank call-centre calls, up to two-thirds by some estimates, are balance checks (S10, grade C, old).
  - A consultancy estimate that 90% of IVR calls are balance checks (S10, grade C).
  - Vendors call balance, transaction and statement enquiries the highest-volume call type (S11, grade C).
- Evidence missing: no Indian bank call mix found. Every source is US-based, old, or a vendor.
- Why "Partly supported": the direction is consistent across several independent writers, but none of them is strong or Indian.
- Do not use the Skit-S2I data for this. The paper says each intent has about 650 train and 100 test samples (S6). Every intent has about the same count because of how it was recorded, so it says nothing about real call volumes.
- What a real person could add: the actual share of simple lookups in an Indian bank's calls.

## H3: Lost-card, block and fraud calls are time-critical

- Evidence for:
  - Under the 2017 rule, zero liability needs the report within 3 working days, and the bank must act immediately on a report to stop further unauthorised transactions (S1).
  - Under the 2026 amendments the window becomes 5 calendar days, and the small-fraud compensation also needs a report to the bank and to the 1930 helpline within 5 days (S2).
  - After 7 working days (old rule) liability depends on the bank's own policy (S1).
- Why "Supported": a regulator ties the customer's financial protection directly to how fast the fraud is reported. That is a grade A source for the cost of delay.
- Careful about what this proves: it proves delay costs the customer money. It does not prove a call must be answered in seconds. The "Urgent lane" is still a design choice.
- Note: the effective date of the new rules is reported differently by different outlets (S2). Until it is confirmed, the app must not quote either window to callers.

## H4: Staff trust a label only if they can see the evidence

- Evidence for: RBI's FREE-AI framework lists "People First" (humans stay in the loop) and "Understandable by Design" among its seven principles, and recommends human oversight for high-risk AI (S5).
- Evidence missing: the framework is advisory, and I read summaries, not the report. It does not say what an agent wants to see on a screen.
- Why "Partly supported": the regulator's direction matches the design (show the original text, the English text and a score, and keep a human for doubtful cases). Nobody has tested whether agents actually want those three items.
- What a real person could add: the questions on the mock-up in `mockup_feedback.md` (M1 to M5).

## H5: Translation and speech errors are the bigger risk

- Evidence for the speech half:
  - Whisper-small raw WER on FLEURS is 86.9% for Hindi and 93.3% for Tamil (S7).
  - Whisper `base` on Common Voice 17 has a WER of 125.6% for Marathi and 167.6% for Telugu (S8).
  - Even Whisper large-v3 is at 80.3% for Marathi and 80.2% for Telugu on the same test (S8).
- Evidence missing for the translation half: I found no study of translation quality on Indian banking terms.
- Also missing: how accurate the classifier will be. That is only known after Phase 6. The classifier works on only 14 classes, and the Skit paper says each class has repeated templates, so I expect it to score high on typed text.
- Why "Partly supported": the speech side is strongly supported. The translation side is untested. I am not claiming the translation side is proven.
- Caution about the numbers: they come from different test sets (FLEURS and Common Voice) and different model sizes, so do not compare one number with another.

## H6: Whisper base is too weak for Indian languages (added after the research)

- Evidence: S7 and S8 above. Whisper `base` produced more errors than reference words for Marathi (125.6%) and Telugu (167.6%), and about nine errors per ten words for Tamil (90.3%). Hindi with IndicWhisper reached 13.6% on one benchmark (S9), which shows the gap between a general model and an Indian-language model.
- Why "Supported": two independent grade A papers show the same pattern.
- Why I added it: the plan says "Whisper first" for Hindi, Marathi, Tamil and others. My smoke test shows Whisper `base` is fast (1.1 s on your laptop), but fast is not useful if the text is wrong.
- What it changes: Phase 4 gets a decision gate (see `targets_and_languages.md`). The English clips will probably work with Whisper `base`. The Indian-language clips probably will not, and IndicConformer or a larger Whisper size is the likely answer.
- Limit of this claim: the papers did not test Indian-accented banking phrases on a phone line. Your own clips in Phase 4 are the real test.

## Findings that change the plan

| # | Finding | Source | What changes |
| --- | --- | --- | --- |
| 1 | The Skit-S2I audio is Indian English recorded over a telephony line at 8 kHz | S6 | The classifier learns English sentence templates. Live Hindi and Marathi calls go through speech recognition and translation first, so the real input will look different. This must go in the data sheet and README as a limit. |
| 2 | Speakers' native languages are Hindi (4), Bengali (3), Kannada (2), Punjabi (1) and Malayalam (1) | S6, and it matches speaker_info.csv | No Marathi, Tamil, Telugu or Urdu voices exist in this data. It does not matter, because we drop the audio. |
| 3 | Whisper `base` is weak on Indian languages | S7, S8 | Phase 4 decision gate. |
| 4 | RBI reporting window is moving from 3 working days to 5 calendar days | S1, S2 | The read-back script must not quote either window. |
| 5 | Published IVR containment examples are 40% to 77%, all from vendors | S11 | The target "under 25% sent to a human" in the plan looks too hard. See `targets_and_languages.md`. |
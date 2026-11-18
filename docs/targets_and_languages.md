# Languages and targets

Date set: 16 November 2026 (before any model is built)

## 1. Language ranking and tiers

"Native speaker found?" is **No** for every row. I did not look for one. So no language can be called a fully validated "core" language yet. The tiers below are provisional, and the promotion rule is at the end of this section.

| Language | Script | Mother-tongue share, Census 2011 (S3) | Speech-recognition evidence | Risk (from plan) | Native speaker found? | Tier now |
| --- | --- | --- | --- | --- | --- | --- |
| English | Latin | About 2.6 lakh as mother tongue; about 10.6% speak it in any capacity (S3b, approximate) | Skit-S2I is Indian English (S6). I found no WER figure. | Low | No | Core (provisional) |
| Hindi | Devanagari | 43.63% | Whisper-small raw WER 86.9% on FLEURS (S7). IndicWhisper 13.6% on one Hindi benchmark (S9). | Low | No | Core (provisional, passes the gate first) |
| Marathi | Devanagari | 6.86% | Whisper WER on Common Voice 17: base 125.6%, small 116.6%, large-v3 80.3% (S8) | Low | No | Core (provisional, passes the gate first) |
| Spanish | Latin | Not applicable | No figure found. Whisper is widely reported as strong on it, but I did not verify that. | Low | No | Demo (provisional) |
| Tamil | Tamil | 5.70% | base 90.3%, large-v3 53.1% (S8); small 93.3% on FLEURS (S7) | Low | No | Experimental |
| Telugu | Telugu | 6.70% | base 167.6%, large-v3 80.2% (S8) | Low | No | Experimental |
| Kannada | Kannada | 3.61% | No figure found | Low | No | Experimental |
| Bengali | Bengali | 8.03% | No figure found | Low | No | Experimental |
| Urdu | Perso-Arabic, right to left | 4.19% | No figure found | Medium | No | Experimental |
| Russian | Cyrillic | Not applicable | No figure found | Low | No | Experimental |
| Manipuri (Meitei) | Meitei Mayek or Bengali script | A scheduled language; I did not look up the share | No figure found | High | No | Experimental |
| Rajasthani | Devanagari | Not a scheduled language. My understanding is that the Census groups it under Hindi, but I did not verify that. | None found | Very high | No | Experimental |

### Why these tiers

| Decision | Reason |
| --- | --- |
| English, Hindi and Marathi are the provisional core | They are the plan's own examples. Hindi is by far the largest group, and Marathi is third-largest (S3). The plan's Phase 3 demo suggestion is also Hindi, Marathi, Spanish and English. |
| Spanish is "Demo" and not "Core" | It is in the plan for breadth, not for the Indian banking audience, and I have no evidence or validator for it. It is a demo language only. |
| Bengali is Experimental even though it is the second-largest | I found no evidence for its speech recognition and have no validator. Size alone does not make a language safe. |
| Tamil and Telugu are Experimental | The published numbers are poor even for large Whisper models (S8). |
| Rajasthani and Manipuri stay Experimental | The plan found no dedicated speech model for them. |
| Russian is Experimental and cut first if time is short | It is not part of the Indian banking audience. |

### Promotion rule (my design, written before the tests)

A language moves up to Core when both of these are true:

1. It passes the Phase 4 gate below.
2. One native speaker has listened to at least 5 sample clips and called the transcripts understandable. A friend or family member is enough for this. It takes about 10 minutes.

## 2. Phase 4 decision gate

Why it exists: the published numbers (S7, S8) say Whisper `base` is likely to fail on Marathi, Tamil and Telugu, and probably on Hindi too.

| Item | Rule |
| --- | --- |
| Test | Record 5 short clips per demo language that each say one banking sentence (for example "my card is lost") |
| Pass | At least 4 of the 5 give a transcript in the correct script that a speaker understands, **and** the English translation contains the banking keyword |
| If Whisper `base` fails for an Indian language | Try Whisper `small`, then `medium`, then IndicConformer 600M (the plan's heavier option). Stop at the first one that passes. |
| If none pass | The language stays Experimental, or is cut |
| Reason for these numbers | Five clips is the smallest set that still shows a pattern, and 4 out of 5 allows one bad recording. This is my judgement, not a published standard. |

## 3. Targets

The first two columns are the plan's placeholders. The "Commit" column is what I will be held to. The reasons are in the last column.

| Tier | Measure | Plan placeholder (stretch) | Commit | Reason |
| --- | --- | --- | --- | --- |
| Core | Correct in the self-serve lane | At least 95% | At least 95% | I kept the plan's number. Self-serve answers are read-only lookups, so a wrong one is a small annoyance, and the read-back catches many mistakes. This is a design choice, not a published benchmark. |
| Core | Recall on urgent intents (classes 8, 12, 13) | At least 98% | See the note below: report "x of y", with zero misses on typed text | A missed urgent call is the costliest error, and a false alarm is cheap because of the read-back. But the test sets are tiny (see below), so a percentage looks more precise than it is. |
| Core | Share of calls sent to a human | Under 25% | **At most 40%** (stretch: under 25%) | Published containment examples run from 40% to 77% (S11) and all come from vendors. Under 25% sent to a human means more than 75% handled by the machine, which is at the top of those examples. Our system also adds four checks (language, speech, translation, classifier), and each can send a call to a person. 40% is realistic for a student prototype. |
| Experimental | All of the above | No pass mark | No pass mark | Same as the plan: measure and publish the numbers. |

### Note on why a percentage for urgent recall is misleading

- Class 8 (fraud) has only 6 unique sentences, and classes 6 and 13 have 8 (from my count of your CSVs).
- After a grouped split of about 30 templates, class 8 will probably have only one template in the test set. With 15 variations per template, that is about 15 rows.
- On 15 rows, one miss is 93.3% recall, and on 30 rows it is 96.7%. So "at least 98%" really means "no misses at all".
- In the live test (10 to 15 spoken sentences per language) there will be only 2 or 3 urgent sentences.
- So I will report urgent recall as a count, like "14 of 15 urgent test rows and 3 of 3 live urgent clips", with the date and the seed. I will not report a percentage as if it were a precise result.

## 4. How each target will be measured

| Target | Measured in | On what data | Honest limit |
| --- | --- | --- | --- |
| Self-serve correctness | Phase 7 and Phase 9 | The 20% held-out part of dataset.csv, and the live sample clips | The held-out text is written by me with the same method as the training text, so the score will look better than real use |
| Urgent recall | Phase 6, 7 and 9 | Same | Tiny sample, see the note above |
| Share sent to a human | Phase 7 | Held-out set plus live clips | Typed text will understate how often real speech goes to a person |

## 5. Change log

| Date | Change | Reason |
| --- | --- | --- |
| 16 Nov 2026 | Added a "Commit" column. Human-review share changed from "under 25%" to "at most 40%", with 25% kept as stretch. | Published containment examples (S11) suggest 25% is too hard for a first version. |
| 16 Nov 2026 | Urgent recall now reported as counts. | Test sets are too small for a percentage. |
| 16 Nov 2026 | Phase 4 decision gate added. | Published Whisper results are poor for Marathi, Tamil and Telugu (S7, S8). |
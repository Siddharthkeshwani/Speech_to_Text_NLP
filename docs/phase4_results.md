# Phase 4 results: speech to text

Date: 18 November 2026
Machine: HP OMEN 16, 24 GB RAM, Intel Core Ultra 7 255H, CPU only, Python 3.11.9
Clips: 10 English, 3 Hindi, 3 Marathi. I recorded them myself. The Hindi and Marathi wording is my own, not checked by a native speaker.

## The gate rule (written before the run)

A language passes with an engine if at least 66% of its clips pass (7 of 10, or 2 of 3). A clip passes if: no error, the transcript is in the right script, and its similarity to the expected text is at least 0.6.

This is weaker than the Phase 1 rule (4 of 5), because there are only 3 clips for Hindi and Marathi.

## Gate summary

| Engine | Language | Clips passed | Clips | Average seconds | Verdict |
| --- | --- | --- | --- | --- | --- |
| whisper-base | English | 10 | 10 | 0.31 | PASS |
| whisper-base | Hindi | 0 | 3 | 1.79 | FAIL |
| whisper-base | Marathi | 0 | 3 | 2.68 | FAIL |
| whisper-small | English | 10 | 10 | 0.99 | PASS |
| whisper-small | Hindi | 3 | 3 | 1.44 | PASS |
| whisper-small | Marathi | 3 | 3 | 8.80 | PASS |
| whisper-medium | English | 10 | 10 | 3.36 | PASS |
| whisper-medium | Hindi | 3 | 3 | 4.85 | PASS |
| whisper-medium | Marathi | 3 | 3 | 32.25 | PASS |

IndicConformer was not needed, because Hindi and Marathi passed on Whisper. It was not tested.

## What the transcripts looked like

English, said and heard:

| Said | Engine | Heard |
| --- | --- | --- |
| Tell me the IFSC code of my branch | base | Till mid-DIFSC code of my branch. |
| Tell me the IFSC code of my branch | medium | Tell me the IFC code of my branch. |
| I want to change my card PIN | base | I want to change my card, ping. |
| I am interested in a home loan | base | I am interested in Home Lun. |
| I want to activate my new card | base | I want to add to it my new code. |
| Please block my UPI ID | small | Please block my UPID. |
| My card is not working at the shop | small | My guide is not working at the shop. |

Hindi (read from the screenshots, to be checked in the CSV):

| Clip | base | small | medium |
| --- | --- | --- | --- |
| hi_lost_card | Urdu-style letters | close but wrong words | correct |
| hi_block_card | mixed junk | extra word at the start, block word wrong | extra word at the start, block word right |
| hi_balance | Urdu-style letters | balance word wrong | correct |

Marathi: `base` wrote Roman letters or a single letter. `small` and `medium` were close in shape, but some words looked Hindi (है instead of आहे) and similarity stayed between 0.69 and 0.80.

## Real speech-to-text errors found

These are real mistakes, so they are good "noise" patterns for the dataset (risk R2) and for the banking word fix in Phase 5.

| Said | Heard |
| --- | --- |
| IFSC | DIFSC, IFC |
| PIN | ping |
| UPI | UPID |
| home loan | Home Lun |
| card | guide |
| activate my new card | add to it my new code |

## Speed against the PRD target

The PRD target is up to 5 seconds for a clip of about 5 seconds.

| Engine | English | Hindi | Marathi | Inside the target? |
| --- | --- | --- | --- | --- |
| base | 0.31 s | 1.79 s | 2.68 s | Yes, but Hindi and Marathi are wrong |
| small | 0.99 s | 1.44 s | 8.80 s | Yes for English and Hindi. Marathi no (one clip took 23.33 s). |
| medium | 3.36 s | 4.85 s | 32.25 s | English yes, Hindi only just, Marathi no (two clips took about 45 s) |

I do not know why Marathi had slow clips. My guess is that Whisper retried the decoding. Not tested.

## Decision for each language

| Language | Engine and size | Status | Tier | Why |
| --- | --- | --- | --- | --- |
| English | whisper small | passed | core | Fewer banking-word mistakes than base, about 1 s |
| Hindi | whisper medium | passed | core | Best on the 3 clips (2 fully correct), 4.85 s |
| Marathi | whisper small | passed (weak) | core (provisional) | Passes the rule but similarity is only 0.69 to 0.73 and one clip took 23 s |
| Tamil, Telugu, Kannada, Bengali, Urdu, Russian | whisper base (default) | untested | experimental | No clips were recorded |
| Spanish | whisper base (default) | untested | demo | No clips were recorded |
| Manipuri | indic-conformer | untested | experimental | No clips, and the code `mni` is not confirmed |
| Rajasthani | whisper medium with the Hindi setting | untested | experimental | No clips |

## Change log

| Date | Change | Reason |
| --- | --- | --- |
| 18 Nov 2026 | English set to small, not base | The rule says base, but base got 4 banking words wrong |
| 18 Nov 2026 | Hindi set to medium, not small | The rule says small, but small got the banking words wrong |
| 18 Nov 2026 | `pytest.ini` now has `testpaths = tests` | pytest was also running smoke_test.py, which showed PASSED even when translation failed |

## Honest limits

1. 3 clips per Indian language is a small sample.
2. One speaker (me) with one microphone, in a quiet room.
3. The expected Hindi and Marathi text is my own wording.
4. The similarity and script checks are a rough stand-in for "a native speaker understands it". Some PASS rows contain a wrong word that matters.
5. I read the Hindi and Marathi transcripts from a terminal that draws them badly. A proper check needs the CSV in VS Code, and ideally a native speaker.
6. Published results (S7, S8) say Whisper is weak for Marathi, Tamil and Telugu. My test agrees for Marathi, and says nothing about Tamil or Telugu.
7. Tiers did not change. Moving to core needs a native speaker to listen to at least 5 clips.
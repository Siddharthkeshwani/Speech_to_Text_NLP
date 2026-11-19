# Phase 5 results: translation to English

Date: 18 November 2026
Machine: HP OMEN 16, 24 GB RAM, Intel Core Ultra 7 255H, CPU only, Python 3.11.9
Translators: Google first, MyMemory as a backup (both through deep-translator)
Speech models used: English small, Hindi medium, Marathi small
Tests: 35 passed (first run), 39 passed after the fixes (fill in after you run them)

## Translation time over 10 calls (first run)

| Measure | Value |
| --- | --- |
| Engine that answered | MyMemory, all 10 calls (Google was blocked) |
| Average seconds | 3.76 |
| Slowest call | 4.73 |
| Fastest call | 3.30 |
| Calls over 2 seconds | 10 of 10 |

PRD target: up to 2 s for translation. This missed it.
Earlier single measurement: 1.84 s with MyMemory (Phase 0). The difference is probably the failed Google try on every call. I changed the code to skip a translator that just failed (see the change log) and I will measure again.

## Translation time after the skip rule (fill in after the rerun)

| Measure | Value |
| --- | --- |
| Engine that answered | MyMemory |
| Call 1 seconds | 8.53 |
| Calls 2 to 10 average seconds | 2.75 |
| Calls over 2 seconds | 4 out of 10 |

## Clip results (first run)

| Language | Clips passed | Clips | Average seconds |
| --- | --- | --- | --- |
| English | 10 | 10 | 0.00 (no translation needed) |
| Hindi | 3 | 3 | 3.91 |
| Marathi | 0 | 3 | 3.63 |

By meaning (my reading): English 10 of 10, Hindi 3 of 3, Marathi 1 of 3. The gate rule counts words, so it passed one wrong word ("guide") and failed one right sentence ("I have lost my card").

## Examples (expected, heard in English)

| Clip | Expected | English we got | Reading |
| --- | --- | --- | --- |
| en_block_upi_01 | Please block my UPI ID | Please block my UPI. | Lost "ID", caused by my glossary rule |
| en_notworking_01 | My card is not working at the shop | My guide is not working at the shop. | Wrong word |
| hi_lost_card_01 | My card is lost | My cart is missing. | Close, one wrong word |
| hi_block_card_01 | I want to block my card | Jeg, I need to block my card. | Right, with an extra word at the start |
| hi_balance_01 | How much balance is in my account | What is the balance in my account? | Right |
| mr_lost_card_01 | My card is lost | I have lost my card. | Right meaning |
| mr_block_card_01 | I want to block my card | My cart is full of books. | Wrong |
| mr_balance_01 | How much balance is in my account | I realised I had got the licence. | Wrong |

## Flags

| Flag | Fired on | What I think |
| --- | --- | --- |
| slow | all 6 non-English clips | Translation took 3.2 to 4.4 s |
| no_banking_word | hi_lost_card_01, mr_block_card_01, mr_balance_01 | All three had a damaged sentence. No false alarms on the clean ones. Only 16 clips, so this is a small sample. |

After the "cart" fix, "My card is full of books" has a banking word, so that flag will not fire for mr_block_card_01 any more. Phase 7 needs a speech check for this.

## Glossary check

| Term | Survived in every clip that had it? | Notes |
| --- | --- | --- |
| IFSC | Yes | en_ifsc_01 |
| UPI | Lost "ID" in en_block_upi_01 | Fixed: "upid" now gives "UPI ID" |
| PIN | Yes | en_pin_01 |
| OTP | Not tested | Not in any clip |

## Mistakes I found and what I did

| Mistake | Fix |
| --- | --- |
| "UPI ID" became "UPI" | "upid" now gives "UPI ID" in glossary.json |
| "card" heard as "cart" (Hindi and Marathi clips) | "cart" gives "card" |
| "card" heard as "guide" (English clip) | "guide" gives "card" |
| "Jeg," at the start of a Hindi sentence | Not fixed. An extra word, and the meaning stays right. |
| Marathi speech text is wrong for 2 of 3 clips | Not fixable in the glossary. Marathi is now experimental. IndicConformer is the next thing to try. |
| Google blocked, so every call wastes time | Skip a failed translator for 120 s |

## Listening check (fill in if you do it)

| Clip | What the listener heard | Matches my expected text? |
| --- | --- | --- |
| hi_lost_card_01 | My card is missing. | My card is lost |
| hi_block_card_01 | Jeg, I need to block my card. |  I want to block my card |
| hi_balance_01 | What is the balance in my account? |  How much balance is in my account |
| mr_lost_card_01 | I have lost my card  | My card is lost |
| mr_block_card_01 | My card is full of items. | I want to block my card |
| mr_balance_01 |  Instead of eating, I'm writing a letter.  | How much balance is in my accoun |

Listener: (name or "friend"), language level: (native or not)

## Decision for each language

| Language | Tier | Status | Why |
| --- | --- | --- | --- |
| English | core | passed | 10 of 10, no translation step |
| Hindi | core (provisional) | passed | 3 of 3, but 2 clips have a wrong or extra word, and no native listener yet |
| Marathi | experimental | weak | 0 of 3 right by meaning. Speech is the problem. |
| All others | unchanged | untested | No clips |

## Change log

| Date | Change | Reason |
| --- | --- | --- |
| 18 Nov 2026 | "upid" now gives "UPI ID" | The old rule deleted "ID" |
| 18 Nov 2026 | Added "cart" and "guide" rules | Real mistakes in 3 clips |
| 18 Nov 2026 | A translator that failed is skipped for 120 s | All 10 calls spent time on a failed Google try (my guess, to be measured) |
| 18 Nov 2026 | Marathi moved from core (provisional) to experimental | 0 of 3 clips right by meaning after translation |

## Privacy

Both translators are online services, so the text of each call goes over the internet. The README and the screen must say this. The offline option (IndicTrans2) is not set up.

## Honest limits

1. Only 16 clips, one speaker, quiet room.
2. The expected English for Hindi and Marathi is my own wording, not checked by a native speaker. I speak a little Hindi and Marathi myself.
3. The glossary only fixes spellings I have already seen. A new speech mistake will not be caught.
4. The similarity rule counts words, not meaning. I read every row myself to fix that.
5. Manipuri has no translator. Rajasthani uses the Hindi setting and was not tested.
6. The 10-call timing is for one short sentence, on one network.
7. Free translation services can block or slow down at any time.
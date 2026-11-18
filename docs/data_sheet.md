# Data sheet: dataset.csv

Date: 17 November 2026

## Where it comes from

- Seed: the text of Skit-S2I (Indian-accented speech to intent dataset). I used the train and test CSV files (11,845 rows). I did not use the audio.
- Skit-S2I has 11 speakers, 14 intents, and was recorded in Indian English over a telephone line at 8 kHz (S6 in research_sources.md).
- Licence: CC BY-NC 4.0, so non-commercial (one GitHub page also says NC-SA, so check before sharing). Text I derived from it inherits the non-commercial limit.

## What I did to it

| Step | Result |
| --- | --- |
| Removed stray spaces and repeats that differ only by capitals | 164 exact texts became 150 unique templates |
| Replaced placeholders (`{{Axis Bank}}`, `<numeric>`, `<Month>`, `(credit/debit)`) with real words | 13 templates affected |
| Made 15 variations per template in three buckets of 5 | 2,250 rows |
| Checked for repeats | 0 exact duplicates. 2,111 different sentences once capitals and punctuation are ignored. |
| Split by template (StratifiedGroupKFold, 5 parts, seed 42, first part is test) | 120 templates (1,800 rows) train, 30 templates (450 rows) test, all 14 classes in test |

## How the variations were written

| Bucket | How | Rows |
| --- | --- | --- |
| 1. Concrete words | The original sentence plus 4 more made by filling placeholders, swapping card or loan types, and adding class-safe endings such as "ending with 4821" | 750 |
| 2. Polite and spoken | Up to one hand-written spoken sentence (112 written, 110 used) plus openers and endings such as "Hello, ..." and "... please". Urgent classes also get "... immediately". | 750 |
| 3. Noise | Lowercase without punctuation, spaced acronyms ("i f s c"), dropped small words, and clumsy translated-style wording | 750 |

## How it was checked

- Automatic: row counts, duplicates, no cleaned sentence in both train and test, all classes in test, and a keyword check (2,244 of 2,250 rows have a keyword for their class; the other 6 are correct hand-written sentences).
- By eye: Claude (an AI) read 126 rows of an earlier build and 84 rows of the final build and fixed the problems found. No human read 20% of the rows, which the plan asks for. This is a gap.

## Known limits

1. Only 150 different base sentences exist. Real callers say many more things.
2. The wording is made by short rules, so it is less varied than real speech. The same openers ("Hello", "Sir", "Madam") appear in many rows.
3. Noise is simulated. It is not real speech-to-text or translation error. Real errors from the sample clips should be added later (risk R2).
4. The original data is Indian English spoken sentences. Live input will be speech in other languages, translated to English.
5. The urgent classes have tiny test sets: class 8 (fraud) has 1 test template (15 rows), class 13 (lost) has 1 (15 rows) and class 12 (block) has 2 (30 rows). Report these as counts.
6. Typos in the source were kept on purpose, for example "uery" and "Perosnal", because real input has typos too.
7. Scores on the test set will be optimistic, because the test sentences are made by the same method as the training ones. The real checks are the unseen-phrasing test and the live speech test in Phase 9.
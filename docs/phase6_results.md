# Phase 6 results: English classifier

Run reviewed on 21 November 2026. Windows HP OMEN project environment.
Data from the Phase 3 guide: 2,250 rows, 150 templates, 14 classes. Grouped split: 1,800 train rows (120 templates), 450 test rows (30 templates).
Exact installed library versions: Cell 1 output was not supplied. Copy its four lines when recording the environment.

## What was built

| Item | Value |
| --- | --- |
| Cleaning | preprocess.py: lowercase, remove punctuation, join spaced letters (ifsc, upi, pin, otp, kyc, emi), remove stop words except not, no, nor, never, cant, cannot, without, lemmatize |
| Vectorizer | TF-IDF on words (1 to 2) plus TF-IDF on character chunks (2 to 4), fitted on training rows only. 4,069 columns before tuning. |
| Baseline | Logistic Regression, max_iter 1000 |
| Tuning | GridSearchCV, 12 combinations, GroupKFold 5, scored by macro F1, training rows only |
| Best settings | C = 100, word n-grams (1, 2), character n-grams (2, 4), grouped CV macro F1 0.9199 |
| Saved | best_model.pkl, vectorizer.pkl, model_info.json |

## Baseline scores on the test rows

| Measure | Value |
| --- | --- |
| Train accuracy | 0.9994 |
| Test accuracy | 0.9689 |
| Macro precision | 0.9688 |
| Macro recall | 0.9452 |
| Macro F1 | 0.9503 |

## Preprocessing experiment (earlier guide reference, Cell 15 output not supplied)

| Join letters | Remove stop words | Accuracy | Macro F1 |
| --- | --- | --- | --- |
| Yes | Yes | 0.9689 | 0.9503 |
| Yes | No | 0.9711 | 0.9455 |
| No | Yes | 0.9644 | 0.9456 |
| No | No | 0.9689 | 0.9421 |

The differences are a few rows out of 450, so this is weak evidence. I kept the first row because it has the best macro F1.

## Model comparison (tuned vectorizer)

| Model | Test accuracy | Test precision | Test recall | Test F1 | Train F1 | Grouped CV F1 | Gap | ms per sentence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.976 | 0.974 | 0.955 | 0.959 | 1.000 | 0.920 | 0.080 | 0.031 |
| Calibrated LinearSVC | 0.978 | 0.978 | 0.960 | 0.965 | 1.000 | 0.903 | 0.097 | 0.038 |
| Naive Bayes | 0.973 | 0.982 | 0.952 | 0.960 | 0.988 | 0.865 | 0.123 | 0.028 |

Chosen: Logistic Regression. Rule: highest grouped CV macro F1. It also has the smallest gap, and it gives probabilities by itself. The test scores of the three are within 2 rows of each other. The saved model is trained on the 1,800 training rows only, not refitted on all rows, so the Phase 7 thresholds stay honest.

## Urgent classes (baseline, test rows)

| Class | Correct |
| --- | --- |
| unauthorised_transaction (8) | 6 of 15 |
| block (12) | 29 of 30 |
| lost (13) | 15 of 15 |
| Any urgent class for a real urgent call | 51 of 60 |

## Mistakes

14 wrong rows of 450 (baseline). The earlier guide’s Cell 14 analysis says 9 of them are variations of one template, "Unauthorised transaction", called past_transactions. Fraud has only 5 training templates, and the US spelling "unauthorized" has 0 rows in the data.

## Are the probabilities honest? (tuned Logistic Regression, test rows)

| Confidence | Rows | Share right |
| --- | --- | --- |
| up to 0.5 | 2 | 100% |
| 0.5 to 0.7 | 12 | 33% |
| 0.7 to 0.9 | 23 | 87% |
| above 0.9 | 413 | 100% |

Average top probability 0.97. Below 0.7 the model is often wrong, and at 0.9 or more it was right on all 413 test rows. Real speech will score lower than typed test rows.

## Does it lean on polite words? (earlier guide reference, Cell 19 output not supplied)

| Bucket | Test accuracy |
| --- | --- |
| 1 (concrete words) | 0.9867 |
| 2 (polite and spoken) | 0.9533 |
| 3 (noisy) | 0.9867 |

196 of 450 test sentences contain an opener word (hello, sir, madam, please, urgent and so on). Removing those words did not change the accuracy (0.9756 and 0.9756).

## Tried on my own sentences and clips

| Check | Result |
| --- | --- |
| 8 sentences I wrote (cell 21) | 6 right. Misses: "I did not make this payment" (card_issue, 0.594), "how much money is in my account" (fraud, 0.703). |
| 16 clips, typed expected English | 15 right. Miss: en_balance_01 (fraud, 0.535). |
| 16 clips, real speech and translation text | 14 right. Misses: English balance → fraud (0.535) and Marathi block → dispatch status (0.748). Marathi balance → balance (0.995) despite a failed translation check. |

Small samples, one speaker. These are not accuracy figures.

## Weak spots

1. Fraud class, short sentences, "unauthorised transaction".
2. The word "money" pulls balance questions toward fraud.
3. "unauthorized" (US spelling) is not in the data.
4. Real speech errors (ping, IFC, UPID, Home Lun, cart, guide) are not in the training data.
5. Marathi balance returned the expected class at 0.995 despite the changed meaning in the supplied translation results.

## Honest limits

1. The test rows are written with the same method as the training rows, so the scores are optimistic. The real checks are the unseen-phrasing test and the live test in Phase 9.
2. Only 150 base sentences.
3. The urgent classes have tiny test sets (15 rows for fraud and lost, 30 for block), so I report counts.
4. The CV score (0.92) is lower than the test score (0.95 to 0.98). Both are shown.
5. The calibrated LinearSVC uses plain 3-fold calibration, not grouped.
6. The saved files only load safely with the same scikit-learn version.

## Decision

Option B chosen on 21 November. Add the training-only Phase 3b examples and rerun the grouped comparison before choosing Phase 7 thresholds.
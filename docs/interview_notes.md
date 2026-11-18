# Interview notes (research log)

Primary interviews done: 0
Why: no time to find and interview people, and I will not invent them.
Instead: I logged what 11 published sources say (all in research_sources.md). Date accessed for all: 16 November 2026.

If I later get even one real conversation, I will add it below as "Interview 1" using the template at the bottom, and I will keep these research entries separate.

## Research entries

### R1: RBI circular on customer liability, 6 July 2017 (S1, grade A)
- What it says (my words): if a customer reports a third-party fraud within three working days, they lose nothing. The bank has to stop further unauthorised transactions as soon as it hears, and must credit the amount back within ten working days. After seven working days, the bank's own policy decides.
- Number: 3 working days, 10 working days, 7 working days.
- Hypothesis it touches: H3.
- What surprised me: the burden of proving the customer is liable sits with the bank, according to the Business Standard report on the circular. I expected the opposite.

### R2: RBI amendment directions, final June 2026 (S2, grade B)
- What it says: the zero-liability window is now five calendar days instead of three working days. There is a new compensation of 85% of the loss, up to Rs 25,000, for frauds up to Rs 50,000, but the customer has to report to the bank and to the 1930 helpline within five days.
- Number: 5 calendar days, 85%, Rs 25,000, Rs 50,000.
- Hypothesis it touches: H3.
- What surprised me: the draft and the final version differ. The draft allowed compensation even after five days, and the final version dropped that. Also, one outlet says the rules start on 1 January 2027 and another says rollout was delayed. I could not settle the date, so I will not quote one.

### R3: Census 2011 mother tongues (S3, grade A)
- What it says: Hindi is 43.63% of the population. Bengali 8.03%, Marathi 6.86%, Telugu 6.70%, Tamil 5.70%, Urdu 4.19%, Kannada 3.61%.
- Hypothesis it touches: H1 and the language ranking.
- What surprised me: Marathi passed Telugu to become the third-largest mother tongue between 2001 and 2011. These numbers are 15 years old now.

### R4: Kantar and IAMAI, Internet in India 2024 (S4, grade B)
- What it says: 886 million active internet users. 57% of urban users prefer Indic languages. 41% of people are offline. 13% of those say the lack of local-language content is a reason.
- Hypothesis it touches: H1.
- What surprised me: it is about content on the internet, not about phone calls. The link to banking IVR is my assumption, so H1 is only "partly supported".

### R5: RBI FREE-AI report, August 2025 (S5, grade B)
- What it says: seven principles, including keeping humans in the loop and making AI understandable. 26 recommendations. It recommends human oversight for high-risk uses.
- Hypothesis it touches: H4.
- What surprised me: it is advisory, not a rule. A bank is not forced to follow it.
- Limit: I read summaries, not the report.

### R6: Skit-S2I paper and dataset card (S6, grade A)
- What it says: 11 speakers, 14 intents, 11,845 samples, recorded over a telephony line at 8 kHz, in Indian English. The sentences were spoken freely from templates.
- Numbers: speakers' native languages are Hindi 4, Bengali 3, Kannada 2, Malayalam 1, Punjabi 1.
- Hypothesis it touches: none directly. It feeds the data sheet in Phase 3.
- What surprised me: the speaker mix matches exactly what I found when I counted speaker_info.csv, so my own count and the paper agree. Also, the audio was recorded over a phone line, which is closer to real bank calls than I expected.

### R7: "What is lost in Normalization?" (S7, grade A)
- What it says: Whisper-small makes a lot of errors on Hindi (86.9% word error rate) and Tamil (93.3%) on the FLEURS test set. The authors say the usual text cleaning makes the scores look better than they are.
- Hypothesis it touches: H5, H6.
- What surprised me: a word error rate can be above 100%, because insertions count as errors too. Malayalam was 287.4%.

### R8: Dolphin paper, Table 7 (S8, grade A)
- What it says: on Common Voice 17, Whisper `base` has a WER of 125.6% for Marathi, 90.3% for Tamil and 167.6% for Telugu. Whisper large-v3 improves to 80.3%, 53.1% and 80.2%.
- Hypothesis it touches: H5, H6.
- What surprised me: even the biggest Whisper model is still above 50% for these three languages.
- Limit: different test set from R7, so I cannot compare the two.

### R9: AI4Bharat Vistaar benchmark (S9, grade B)
- What it says: on the Hindi subset, IndicWhisper averages 13.6% WER and NVIDIA's large model 18.6%.
- Hypothesis it touches: H6.
- What surprised me: an Indian-language model gets about 13.6% on Hindi, while general Whisper-small gets 86.9% on a different set. The two numbers use different test sets, but the gap is big enough to matter.
- Limit: I am reading the last column of a table as the average.

### R10: Call mix for balance checks (S10, S11, grade C)
- What it says: older US sources say over half of bank call-centre calls are balance checks. Vendors say balance, transaction and statement queries are the highest-volume call type.
- Hypothesis it touches: H2.
- What surprised me: nothing Indian turned up. Every source is from the US or from a vendor.

### R11: IVR containment examples (S11, S12, grade C)
- What it says: one global bank's IVR contained about 40% of callers, and 52% after adding a virtual assistant. A US regional bank had 42.4% on voice. Another bank reported 77.35%. One vendor claims 20 to 35% for good Indian IVRs.
- Hypothesis it touches: the target "under 25% sent to a human".
- What surprised me: the numbers are all over the place, and all of them come from companies selling these systems. I would not call any of them a benchmark.

## Questions desk research could not answer

These are the questions I would ask a real person if I ever get 20 minutes. I am listing them so the gap is visible and not hidden.

| # | Question | For whom | Hypothesis |
| --- | --- | --- | --- |
| Q1 | What share of your calls are simple lookups such as balance, IFSC code or branch address? | Contact-centre agent or supervisor | H2 |
| Q2 | What happens today when a caller cannot find the right menu option, or speaks a regional language? | Agent | H1 |
| Q3 | When someone calls about a lost card, how long until they reach the person who can block it? | Agent | H3 |
| Q4 | If a machine gave you a label for a call, what would you want to see beside it before trusting it? | Agent or supervisor | H4 |
| Q5 | Which banking words would you never expect a machine to get right in your language? | Native speaker | H5 |
| Q6 | Do people mix English and your language in one sentence when talking about banking? | Native speaker | H5 and the out-of-scope list |

## Template for a real interview (empty, for later)

```
### Interview [number]

- Date:
- Role:
- Language(s):
- How (call, in person):
- What they said (my own words):
  -
  -
- Any number they gave (and whether it is a guess):
- Hypothesis it touches (H1 to H6):
- What surprised me:
```
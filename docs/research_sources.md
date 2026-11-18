# Research sources

Date accessed: 16 November 2026
How I did it: desk research only. No primary interviews or surveys were done.

## How to read the grades

| Grade | Meaning | How much I trust it |
| --- | --- | --- |
| A | Regulator, government data, peer-reviewed or arXiv paper, dataset card | High, but still check the date |
| B | News report or industry body that summarises primary data | Medium. I did not read the original document |
| C | Vendor blog or case study, or an old article from another country | Low. Direction only, never a headline number |

## Sources I used

| ID | Source | What I took from it | Grade |
| --- | --- | --- | --- |
| S1 | RBI circular DBR.No.Leg.BC.78/09.07.005/2017-18, 6 July 2017, "Customer Protection - Limiting Liability of Customers in Unauthorised Electronic Banking Transactions". https://rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx?Id=11040 | Zero liability if a third-party breach is reported within 3 working days. On a report, banks must take immediate steps to stop further unauthorised transactions. Banks must credit (shadow reversal) the amount within 10 working days. After 7 working days liability follows the bank's policy. | A |
| S2 | RBI amendment directions on limiting customer liability in digital transactions (draft 6 March 2026, final notified around 24 to 25 June 2026). I read news reports, not the RBI PDF: Moneylife 25 June 2026 (https://moneylife.in/article/rbi-notifies-digital-fraud-compensation-rules-gives-banks-more-time-delays-rollout/80882.html), Business Standard (https://www.business-standard.com/markets/capital-market-news/rbi-issues-amendment-directions-on-review-of-framework-of-limiting-customer-liability-in-digital-transactions-126062500400_1.html), Outlook Money (https://www.outlookmoney.com/banking/who-pays-when-a-digital-fraud-takes-place-rbi-shifts-burden-of-proof-to-banks) | Zero liability for third-party breaches reported within 5 calendar days (was 3 working days). Compensation of 85% of net loss up to Rs 25,000 for small frauds (gross loss up to Rs 50,000), with reporting to the bank and the 1930 helpline within 5 days. Outlook Money reports the effective date as 1 January 2027. Moneylife's headline says the rollout was delayed. **I could not confirm the date, so check rbi.org.in before quoting it.** | B |
| S3 | Census of India 2011 mother-tongue table, as given in the Ministry of Home Affairs reply in Lok Sabha, 16 March 2021 (PDF). https://xn--i1b5bzbybhfo5c8b4bxh.xn--11b7cb3a6a.xn--h2brj9c/MHA1/Par2017/pdfs/par2021-pdfs/LS-16032021/292.pdf | Share of population by mother tongue: Hindi 43.63%, Bengali 8.03%, Marathi 6.86%, Telugu 6.70%, Tamil 5.70%, Urdu 4.19%, Kannada 3.61%. | A |
| S3b | A secondary page repeating Census figures (https://www.telangana360.com/2025/12/the-constitution-of-india-part-xvii.html) and a news summary (https://thelogicalindian.com/news/hindi-fastest-growing-language) | About 129 million people (10.6%) report speaking English in any capacity; only about 2.6 lakh report it as their mother tongue. Treat the 10.6% as approximate. | C |
| S4 | Kantar and IAMAI, "Internet in India 2024" (https://www.iamai.in/sites/default/files/research/Kantar_%20IAMAI%20report_2024_.pdf), plus coverage in Business Today (https://www.businesstoday.in/amp/technology/news/story/indias-internet-revolution-key-insights-from-kantar-and-iamai-report-461043-2025-01-16) | 886 million active internet users. 57% of urban internet users prefer to access the internet in Indic languages. 41% of the population is offline, and 13% of those people give "no local-language content" as a reason. | B |
| S5 | RBI FREE-AI committee report, August 2025, read through summaries only (KPMG https://kpmg.com/in/en/insights/2025/09/rbis-free-ai-committee-report-in-the-financial-sector.html, Securiti, GS Times) | Seven principles including "People First" (humans stay in the loop) and "Understandable by Design" (explainability). 26 recommendations, including human oversight for high-risk AI. The framework is advisory, not binding. | B |
| S6 | Skit-S2I paper (arXiv 2212.13015, https://arxiv.org/pdf/2212.13015), the Hugging Face dataset card (https://huggingface.co/datasets/skit-ai/skit-s2i) and the GitHub README | 11 speakers (8 female, 3 male), 14 intents, 11,845 samples, about 650 train and 100 test samples per intent. Indian English, recorded over a telephony line at 8 kHz. Sentences were spoken freely from templates. Licence CC BY-NC 4.0 (one GitHub page also says NC-SA, so verify). | A |
| S7 | "What is lost in Normalization?" (arXiv 2409.02449, https://arxiv.org/pdf/2409.02449) | Whisper-small on the FLEURS test set, raw word error rate (WER): Hindi 86.9%, Tamil 93.3%, Malayalam 287.4%. The authors argue that Whisper's text normalisation makes Indic scores look better than they really are. | A |
| S8 | Dolphin paper (arXiv 2503.20212, https://arxiv.org/pdf/2503.20212), Table 7 (Common Voice 17) | Whisper WER, Marathi: base 125.6%, small 116.6%, large-v3 80.3%. Tamil: base 90.3%, large-v3 53.1%. Telugu: base 167.6%, large-v3 80.2%. A WER above 100% means more errors than words in the reference. | A |
| S9 | AI4Bharat Vistaar benchmark (https://github.com/AI4Bharat/vistaar) | On the Hindi subset, IndicWhisper averages 13.6% WER against 18.6% for NVIDIA's large model. I am reading the last column of the table as the average. | B |
| S10 | Retail Banker International article on mobile banking and call centres (https://www.retailbankerinternational.com/?p=8838). US data, undated and old. | Over half of bank call-centre calls, up to two-thirds by some estimates, are balance checks. One consultancy estimated that 90% of IVR calls are balance checks. | C |
| S11 | Kore.ai blog (https://www.kore.ai/blog/top-use-cases-for-voice-ai-agents-in-banking), Kore.ai case study (https://info.kore.ai/multinational-banking-leader-deploys-ai-powered-smart-call-deflection-to-unclog-its-contact-centers-achieves-70-reduction-in-call-waiting-time), Cognizant case study (https://www.cognizant.com/us/en/case-studies/leading-bank-scales-customer-service-with-cloud-and-ai) | Balance, transaction and statement enquiries are described as the highest-volume call type. One global bank's IVR contained about 40% of callers, rising to 52% after a virtual assistant. Voice containment of 42.4% at a US regional bank. One bank reached 77.35% containment. These are all vendors writing about their own work. | C |
| S12 | caller.digital blog (https://caller.digital/blog/voice-ai-vs-ivr-india-banks-cio-decision) | Claims good Indian bank IVRs reach 20 to 35% deflection for routine enquiries. A vendor claim with no stated method. | C |

## Claims I found and deliberately did NOT use

Several vendor blogs quote statistics with a made-up-looking source. I could not trace any of these to the original document, so I left them out.

| Claim seen | Where | Why I rejected it |
| --- | --- | --- |
| "Only 36% of rural Indians are comfortable banking in English or Hindi (RBI report 2023)" | gnani.ai blog | No RBI report with this number could be found, and the blog gives no title |
| "88% of Indians prefer regional languages (KPMG)", "68% prefer native language for finance", "60% of rural customers struggle with English (RBI 2022)" | oriserve.com, reverieinc.com and similar blogs | Same problem: no traceable original, and the numbers do not agree with each other |
| "95%+ recognition accuracy across 50+ regional accents (NASSCOM 2023)" | oriserve.com blog | A vendor marketing line. Published WER numbers in S7 to S9 look very different |
| "Average IVR abandonment of 20 to 30% (or 35 to 55%) in Indian banks" | callmissed.com and caller.digital blogs | The two blogs give different ranges, and neither shows its method |

## Things I could not find

- Any published breakdown of call types for an Indian bank's contact centre.
- Any study of how Indian bank agents react to ML labels on a screen.
- Word error rates for Whisper on Spanish, Russian, Kannada, Bengali, Urdu, Manipuri or Rajasthani in the sources I read.
- Any published translation-quality test on Indian banking terms such as IFSC, UPI and OTP.
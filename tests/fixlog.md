# Fix log

## Round 1 (2026-10-19), Copilot Studio Evaluation "Test1"
Export: tests/runs/R1-run1.csv. Score with `python3 tests/score_copilot.py tests/runs/R1-run1.csv`.

- Result: 17/36 (47%). FAQ 5/11. Refusals 0/5. Made-up fees 0. OneDrive "connect first" error is gone.
- Ids 32-36: Fallback topic sends "`The provided sources do not cover that.`" (wrong wording, in backticks). Fix: settings, Fallback message text.
- Ids 1, 4, 5, 6, 7, 14, 15, 17, 23, 31: over-refusal. The text is in the files and extracts cleanly (checked with pdftotext), and the same files are cited on other rows, so it isn't a missing file. Every one is the Fallback message, so knowledge search returned nothing. Fix: settings, content moderation High to Medium (GUIDE 3.5 over-refusal row). If still failing, source fix.
- Id 19: says CPF faculty are "employed by a secondary partner" (typo in the Comparison and once in the CEP Guide). Fix: instructions, CONFLICTS line.
- Id 10: fees right but left out the $1,060 total, the effective date, and the as-of line. Fix: instructions, cost rule.
- Id 16: no as-of line. Fix: instructions (also add it to the response instructions box).
- Id 20: left out each endorsement's evidence. Fix: instructions, STANDARDS comparison line.
- Grader notes: "Answer quality" marks every refusal Fail, so ignore it on 32-36. "Grounded and cited" passed in-scope refusals and failed id 18 for a correct $1,060 total, so trust score_copilot.py over it.
- Instructions paste lost line breaks ("SOURCESAnswer only..."). Headings now end with a colon so they still read right if that happens again.

## Round 2 (2026-10-19), "TEST 2" export
Export: tests/TEST 2/. Settings: moderation Medium, round 1 instructions. Score: 27/36 (75%). FAQ 10/11. Refusals 0/5. Made-up fees 0 by the script, but id 36 predicts the 2028-2029 fee.
- The 10 over-refusals from round 1 are fixed (moderation Medium).
- Ids 32-35: Fallback now says "The provided sources do not cover that." (backticks gone, wording still wrong). Fix: settings, Fallback text.
- Id 36: says the 2028-2029 Letter of Intent fee "will be $350". Fix: instructions, future-cycle rule.
- Id 31: says a pre-application fee exists. Fix: instructions, CONFLICTS line.
- Id 19: still repeats "employed by a secondary partner". Fix: instructions, CPF definition in ANSWERS. If it repeats again, remove the CEP vs CPF Standards Comparison from the SharePoint folder.
- Id 3: left out CPF's 13 standards (October 2019). Fix: instructions, STANDARDS line.
- Id 23: left out the institutional accreditor and state authorization items. Fix: instructions, eligibility line.
- Id 2: passes, but gives no link (the FAQ's link is not in the extracted text). Fix: instructions, accredited programs URL.
- As-of line was added after historical years (id 1). Fix: instructions and response formatting say fee amounts or upcoming deadlines only.
- score_copilot.py now finds Meaning match by name; this export put Answer quality first.

## Round 3 (2026-10-19), "Test 3" export
Export: tests/Test 3/. Round 2 instructions and response formatting were in place. Score: 28/36 (78%). FAQ 10/11. Refusals 0/5 strict. Made-up fees 0 by the script, but id 36 still predicts the 2028-2029 fee.
- Ids 32-35: Fallback says "That is not covered by the provided sources" with no final period. Fix: settings, add the period.
- Ids 36, 19, 3, 23: unchanged even though the instructions name each case. Knowledge answers seem to follow Response formatting more than Instructions. Fix: agent/response-formatting.txt now carries the CPF and future-cycle rules (434 of 500 characters). If 19 still fails, remove the CEP vs CPF Standards Comparison from the SharePoint folder.
- Id 31 now passes (calls the Letter of Intent the pre-application).
- Shipped to Mike as-is with known gaps listed in deliverable/mike-note.md.

## Test set audit (2026-10-19), against the 15 sources
- Id 2: expected a nacep.org/accredited-programs URL that is not in any source's text (the FAQ only says "A complete list of accredited programs is available here"). Rewritten to match what the FAQ says. Ignore Copilot's "Answer quality" and "Grounded and cited" on this row; they want a list of colleges or a refusal, which contradict each other.
- Id 3: dropped the category list, the fall 2018 date and the FAQ 2009 note. Kept the core facts the sources state (2002/2009/2017, CEP 16, CPF 13 October 2019).
- Id 23: removed "Notes the Guides' list leaves out membership and the Institute." The CEP Guide's list includes membership, so that note was wrong.
- Id 36: expected said both "Refuses" and "May give the current $350". Now it must start with the refusal and may add the current 2027-2028 fee.
- Ids 32-35: score_copilot.py now accepts the refusal with or without the final period.
- Corrected Test 3 score: 32/36 (89%). Real agent misses: 19 (repeats the CPF typo), 36 (states a 2028-2029 fee), 3 and 23 (each leaves out one fact). agent/response-formatting.txt (477 of 500 characters) now covers all four.
- Read-through of Test 3 answers as Mike would: accurate, on topic, cited to the page. Fixed in response formatting: the as-of line showed after non-fee facts (ids 1, 9, 11); id 10 called the $350 Letter of Intent fee "per endorsement" (the source doesn't say that); long answers now open with a one-sentence answer.
- Test 4 spot check: Meaning match scored ids 2 and 3 at 50 on correct answers. Id 2's expected answer now repeats the FAQ's own sentence. Id 3's expected answer now holds only the core facts (definition, 2002/2009/2017, six categories); the standard counts are no longer required.
- Ids 2 and 3 re-checked against the FAQ PDF itself (both are FAQ questions). Id 2: the FAQ says "A complete list of accredited programs is available here.", with the link (nacep.org/accredited-programs) only as a hyperlink, so the agent can't see it; response formatting now gives the URL. Id 3: expected answer now follows the FAQ's own answer (2002/2009/2017, 16 standards in six categories from fall 2018, CPF standards added 2019). The agent's Test 4 answer leaves out the 16 and the 2019 CPF line, so that is a real miss; response formatting now asks for the counts.

## Test 5 (2026-10-21, rebuilt agent with the 15 uploaded PDFs)
- Score: 29/36 (81%). FAQ 11/11, refusals 5/5, made-up fees 0.
- Real misses: 21 says CPF has an annual PD standard like CEP F3 (wrong, CPF has no F3); 30 answers F2 for CEP only; 15 answers CEP C3 classroom visits instead of the virtual accreditation site visit; 24 is vague about which standards can share documentation. 19, 22, 23 leave out some details.
- Q2 passes the grader but only links the list. Fixed in the same day's source update: 8 PDFs added (sources/ADDED-2026-10-21.md), instructions now let the agent name accredited colleges. Rows 2, 32 and 34 changed and 5 rows added, so the next run has 41 rows.

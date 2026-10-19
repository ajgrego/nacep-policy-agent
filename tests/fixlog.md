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

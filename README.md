# NACEP policy agent

**Archived 2026-10-28.** The NACEP Accreditation Assistant (Copilot Studio) for Mike Beam. Built, tested over 6 rounds, and sent to Mike to evaluate. Kept as a reference for any future Copilot Studio knowledge agent. The vault's summary: `archive/nacep-agent/README.md` in `ajgrego/USI`.

## What's here
- `deliverable/rebuild-checklist.md`: rebuild the agent in a new environment, paste-ready. **Start here** to stand it up again.
- `deliverable/mike-note.md`: the note sent to Mike.
- `agent/instructions.md` and `agent/response-formatting.txt`: what to paste into Copilot Studio.
- `sources/files/`: the 23 NACEP PDFs uploaded as Knowledge (retrieved 2026-10-19 and 2026-10-21, see `sources/ADDED-2026-10-21.md`).
- `tests/`: `copilot-test-set.csv` (41 rows, import into Evaluate), `gold.csv` (answer key), `score_copilot.py`, `fixlog.md` (what each test round found and fixed), and the exported runs.
- `GUIDE.md`: the original full build guide (Oct 19).

## Where it ended
Test 5: 29/36. Test 6 ran the old 36-row set; re-import `copilot-test-set.csv` before another run. Open misses are listed at the end of `tests/fixlog.md`.

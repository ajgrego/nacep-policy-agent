---
type: guide
tags: [nacep, copilot-studio, accreditation, testing, guide]
created: 2026-10-19
---
# NACEP agent: build, test, deliver (by hand)

Mike Beam's ask (Teams, 2026-10-07): a Copilot Studio agent that's an expert on NACEP accreditation, his 5 pages as closed context, other NACEP material if relevant, the FAQ as the starting test set, and he validates the answers. Request: [[emails/2026-10-07-nacep-accreditation-agent|Mike's Teams chat]]. Earlier notes: [[notes/nacep-accreditation-agent|NACEP agent guide]], [[notes/nacep-agent-quickstart|quick start]], [[tasks/nacep-accreditation-agent|task]].

Heads up: Mike is listed as an Accreditation Commissioner in the CPF Guide acknowledgments (p. 2). He knows this material. Expected answers have to be exact.

Tool: **Copilot Studio** (Mike said "use studio"). No choice to make.

| Step | What | Time |
|---|---|---|
| 0 | Repo setup | 10 min |
| 1 | Sources and source log | 60 min |
| 2 | Build the agent | 30 min |
| 3 | Test, score, fix | 2.5 to 3.5 hr |
| 4 | Note for Mike and send | 30 min |
| | **Total** | **about 5 hr** |

---

## 0. Repo setup (10 min)

0.1 If `nacep-policy-agent` doesn't exist yet: github.iu.edu > **+** > **New repository** > name `nacep-policy-agent` > **Private** > **Add a README** > **Create repository**. Then add it to Obsidian Git the same way as your other synced repos.

0.2 Make the folders. All paths in this guide are from the repo root.
```
cd <path to nacep-policy-agent>
mkdir -p sources/files agent tests/runs deliverable
touch sources/SOURCES.md agent/instructions.md agent/settings.md tests/gold.csv tests/results.csv tests/fixlog.md deliverable/mike-note.md
```

Layout when done:
```
sources/files/        the exact files you upload to Copilot Studio (and nothing else)
sources/SOURCES.md    source log
sources/checksums.txt sha256 of every source file
agent/instructions.md the system instructions, as pasted
agent/settings.md     name, description, settings, model, publish dates
tests/gold.csv        gold question set
tests/copilot-import.csv  2-column copy for the Evaluate tab
tests/score.py        scoring script
tests/results.csv     every scored answer, every run
tests/runs/           raw exports from each run
tests/fixlog.md       one entry per fix round
deliverable/          note and test sheet for Mike
```

All content is public NACEP material. No IU data goes in this repo.

---

## 1. Sources (60 min)

### 1.1 Download (30 min)
Save every file into `sources/files/` with the exact name in the table. The file name is what the agent shows as its citation, so don't shorten it.

**Web pages** (rows 1 to 5 and 15): open in Chrome > **Ctrl+P** > Destination **Save as PDF** > **More settings** > tick **Headers and footers** (stamps the URL, date and page number on every page) > untick **Background graphics** > **Save**.
**PDFs on nacep.org** (rows 6, 7, 12 to 14): open the link > download icon top right > save with the table name.
**Box links** (rows 8 to 11): open the link > **Download** (top right). If it opens a folder, click the file you want first, then **Download**. No Box login should be needed. If it asks for one, skip that file and write "not retrievable, Box login required" in the log.

| # | Save as (`sources/files/`) | URL |
|---|---|---|
| 1 | `NACEP Standards for Quality.pdf` | https://www.nacep.org/accreditation/standards/ |
| 2 | `NACEP About Us.pdf` | https://www.nacep.org/about-nacep/ |
| 3 | `NACEP Accreditation Commission Overview.pdf` | https://www.nacep.org/accreditation/accreditation-commission/ |
| 4 | `NACEP Accreditation FAQ.pdf` | https://www.nacep.org/accreditation/accreditation-faq/ |
| 5 | `NACEP Application Process and Resources.pdf` | https://www.nacep.org/accreditation/process-timeline-cost/ |
| 6 | `NACEP CEP Accreditation Guide v7 rev 8-2026.pdf` | https://www.nacep.org/docs/accreditation/CEP-Accreditation%20Guide-SINGLE-PAGE-11-2022%20Rev%205-2024.pdf |
| 7 | `NACEP CPF Accreditation Guide v2 Nov 2022.pdf` | https://www.nacep.org/docs/accreditation/Website/CPF-Accreditation%20Guide-SINGLE-PAGE-11.2022.pdf |
| 8 | `NACEP CEP vs CPF Standards Comparison.pdf` | https://nacep.app.box.com/file/1509899257236?s=bnk6j40ewl5xnsj9pzq6jjlthuohasrw |
| 9 | `NACEP Self-Study Assessment Worksheet CEP.pdf` (and `...CPF.pdf` if the folder has a separate one) | https://nacep.box.com/s/nnyiasuv27jr1co92modbig07y7zye8b |
| 10 | `NACEP Virtual Site Visit Guide and Agenda.pdf` | https://nacep.box.com/s/3os7242mrqv3qvj9rp2595rknya1gp4e |
| 11 | `NACEP Electronic Application Requirements Guide.pdf` (guide only, skip blank forms) | https://nacep.box.com/s/tguijfz3r25a4sbxqwatafp0ywp0t2b7 |
| 12 | `NACEP Evaluation Guide Sep 2019.pdf` | https://www.nacep.org/docs/accreditation/Website/NACEPEvaluationGuide9.16.19.pdf |
| 13 | `NACEP Survey Guide.pdf` | https://www.nacep.org/docs/accreditation/Website/NACEPSurveyGuide.pdf |
| 14 | `NACEP Classroom Visit Issue Brief Sep 2019.pdf` | https://www.nacep.org/docs/accreditation/IssueBrief%20-TheClassroomVisit9.6.19Final2.pdf |
| 15 | `NACEP What Is Concurrent Enrollment.pdf` | https://www.nacep.org/about-nacep/what-is-concurrent-enrollment/ |

Rows 1 to 5 are Mike's pages. 6 and 7 are linked from his Standards page and hold the actual standard text and evidence. 8 to 15 are linked from his pages and fill process gaps (self-study, site visit, survey, evaluation).

If a Box file is Word or Excel, keep it as is if it's .docx. If it's .xlsx, open it and **File > Export as PDF**, because spreadsheets index poorly.

**Leave out** (link only, the agent can point to them): CEP and CPF Summary Guides (repeat the full Guides, duplicate text hurts retrieval), accredited programs list and Accreditation Institutes calendar (change often), Commission members page (named people), join, volunteer, conference and Letter of Intent login pages, Evaluation Toolkit site, District HS Guide, other issue briefs, naceplearning.org.

### 1.2 Check every file (10 min)
```
cd sources/files
for f in *.pdf; do printf '\n== %s\n' "$f"; pdfinfo "$f" | grep -E 'Pages|ModDate'; pdftotext -l 2 "$f" - | head -8; done
sha256sum * > ../checksums.txt
```
- Empty text under a file = scanned image. The agent can't read it. Drop it and log "scan, excluded".
- Garbled text = same thing.
- `checksums.txt` lets you prove later which exact file the agent was tested on.

Page numbers: cite the number printed in the page footer, not the PDF viewer's page. CEP Guide: PDF page = printed page + 5. CPF Guide: PDF page = printed page + 3.

### 1.3 Source log (20 min)
Paste into `sources/SOURCES.md`, then fill every `__`. Rows 1 to 7 are pre-filled from the copies you already checked. For 8 to 15, skim the file and write the version and 2-line summary. While skimming the 2019 documents, note anything that conflicts with the newer pages (fees, deadlines, standard counts). Those go in the CONFLICTS part of the instructions in step 2.
```
# Sources

Knowledge files for the NACEP Accreditation Assistant (Copilot Studio). Files in `sources/files/`, checksums in `checksums.txt`.
Rule: add a file only if its content isn't already in the set. Duplicate text crowds out the right passages at retrieval.

## 1. NACEP Standards for Quality.pdf
- URL: https://www.nacep.org/accreditation/standards/
- Retrieved: 2026-10-__
- Version: web page, no version. Retrieval date printed in footer.
- Summary: CEP standards (16 in six categories, adopted 2002, revised 2009 and 2017) and CPF standards (13, adopted October 2019). Links to both Accreditation Guides, the Summary Guides and the CEP vs CPF comparison.

## 2. NACEP About Us.pdf
- URL: https://www.nacep.org/about-nacep/
- Retrieved: 2026-10-__
- Version: web page, no version.
- Summary: What NACEP is, its vision, mission, values, four areas of work and policy platform. No accreditation process detail.

## 3. NACEP Accreditation Commission Overview.pdf
- URL: https://www.nacep.org/accreditation/accreditation-commission/
- Retrieved: 2026-10-__
- Version: web page, no version.
- Summary: Why accreditation matters and its benefits, the Commission's role and who can serve on it. How to file a complaint.

## 4. NACEP Accreditation FAQ.pdf
- URL: https://www.nacep.org/accreditation/accreditation-faq/
- Retrieved: 2026-10-__
- Version: web page, no version. Oldest source in the set.
- Summary: 11 Q&As on history, standards, benefits, process, timing, eligibility, cost and denial. Out of date on 17 standards, the pre-application fee, CPF "will open" and summer deadlines.

## 5. NACEP Application Process and Resources.pdf
- URL: https://www.nacep.org/accreditation/process-timeline-cost/
- Retrieved: 2026-10-__
- Version: web page. Fees effective September 1, 2026. Letter of Intent due December 1, 2026 for the 2027-2028 cycle.
- Summary: Eligibility, fees, the 24-month cycle and the 7 steps from self-study to maintenance. Main source for fees, dates and process.

## 6. NACEP CEP Accreditation Guide v7 rev 8-2026.pdf
- URL: https://www.nacep.org/docs/accreditation/CEP-Accreditation%20Guide-SINGLE-PAGE-11-2022%20Rev%205-2024.pdf
- Retrieved: 2026-10-__
- Version: cover says November 2022, Version 7, Rev 8-2026. PDF modified 2026-08-25. URL and link text still say Rev 5-2024. Cover wins.
- Summary: Standard text, required evidence and commentary for all 16 CEP standards. Also eligibility, multi-campus programs and applying for both endorsements (pp. 6 to 7).

## 7. NACEP CPF Accreditation Guide v2 Nov 2022.pdf
- URL: https://www.nacep.org/docs/accreditation/Website/CPF-Accreditation%20Guide-SINGLE-PAGE-11.2022.pdf
- Retrieved: 2026-10-__
- Version: November 2022, Version 2.
- Summary: Standard text, required evidence and commentary for the 13 CPF standards. p. 1 has the three readiness questions and what can be shared with a CEP application.

## 8. NACEP CEP vs CPF Standards Comparison.pdf
- URL: https://nacep.app.box.com/file/1509899257236?s=bnk6j40ewl5xnsj9pzq6jjlthuohasrw
- Retrieved: 2026-10-__
- Version: __
- Summary: __

## 9. NACEP Self-Study Assessment Worksheet CEP.pdf
- URL: https://nacep.box.com/s/nnyiasuv27jr1co92modbig07y7zye8b (the Application Process page uses this same link for both the CEP and CPF worksheet)
- Retrieved: 2026-10-__
- Version: __
- Summary: __

## 10. NACEP Virtual Site Visit Guide and Agenda.pdf
- URL: https://nacep.box.com/s/3os7242mrqv3qvj9rp2595rknya1gp4e
- Retrieved: 2026-10-__
- Version: __
- Summary: __

## 11. NACEP Electronic Application Requirements Guide.pdf
- URL: https://nacep.box.com/s/tguijfz3r25a4sbxqwatafp0ywp0t2b7
- Retrieved: 2026-10-__
- Version: __
- Summary: __

## 12. NACEP Evaluation Guide Sep 2019.pdf
- URL: https://www.nacep.org/docs/accreditation/Website/NACEPEvaluationGuide9.16.19.pdf
- Retrieved: 2026-10-__
- Version: 9.16.19 (from file name). Cover: __
- Summary: __

## 13. NACEP Survey Guide.pdf
- URL: https://www.nacep.org/docs/accreditation/Website/NACEPSurveyGuide.pdf
- Retrieved: 2026-10-__
- Version: __
- Summary: __

## 14. NACEP Classroom Visit Issue Brief Sep 2019.pdf
- URL: https://www.nacep.org/docs/accreditation/IssueBrief%20-TheClassroomVisit9.6.19Final2.pdf
- Retrieved: 2026-10-__
- Version: 9.6.19 (from file name). Cover: __
- Summary: __

## 15. NACEP What Is Concurrent Enrollment.pdf
- URL: https://www.nacep.org/about-nacep/what-is-concurrent-enrollment/
- Retrieved: 2026-10-__
- Version: web page, no version.
- Summary: __

## Excluded (link only)
CEP and CPF Summary Guides (duplicate the Guides), accredited programs list, Accreditation Institutes calendar, Commission members, join/volunteer/conference pages, Letter of Intent login, Evaluation Toolkit, District HS Guide, other issue briefs, naceplearning.org.

## Known conflicts
- FAQ: 17 standards in five categories (2009 version). Current CEP is 16 in six.
- FAQ: "pre-application fee". Now the Letter of Intent ($350).
- FAQ: CPF "will open" in 2022-23. It's open.
- FAQ and CPF Guide p. 6: summer application and deadlines. Now Letter of Intent December 1 and a 24-month cycle.
- Guides' eligibility list leaves out NACEP membership and the Accreditation Institute. Application Process page has the full list.
- From 2019 docs: __
```

Commit: Obsidian **Ctrl+P** > `Obsidian Git: Commit-and-sync`. Message: `sources: 15 NACEP files and source log`.

---

## 2. Build the agent (30 min)

2.1 **Instructions file.** Paste the block below into `agent/instructions.md`. Replace both `<RETRIEVAL DATE>` with the date from your log (for example `2026-10-20`). Add any conflicts you found in 1.3 under CONFLICTS. Check the length is under 8,000 characters:
```
wc -m agent/instructions.md
```

```
You are the NACEP Accreditation Assistant. You answer questions about NACEP (National Alliance of Concurrent Enrollment Partnerships) accreditation for IU staff.

SOURCES
Answer only from your uploaded knowledge files. Never use the web, your training data, or general knowledge, even when you think you know the answer.
The files were retrieved from nacep.org on <RETRIEVAL DATE>:
- Web pages: NACEP Standards for Quality, NACEP About Us, NACEP Accreditation Commission Overview, NACEP Accreditation FAQ, NACEP Application Process and Resources, NACEP What Is Concurrent Enrollment.
- Accreditation Guides: NACEP CEP Accreditation Guide (Version 7, Rev 8-2026) and NACEP CPF Accreditation Guide (Version 2, November 2022). These are the authority on standard text, required evidence, and commentary.
- Supporting documents: NACEP CEP vs CPF Standards Comparison (use only for CEP vs CPF differences), NACEP Self-Study Assessment Worksheets, NACEP Virtual Site Visit Guide and Agenda, NACEP Electronic Application Requirements Guide, NACEP Evaluation Guide (September 2019), NACEP Survey Guide, NACEP Classroom Visit Issue Brief (September 2019).

CITATIONS
End every sentence or bullet that states a fact with a citation in square brackets.
- Guides and other PDF documents: [file name, p. N], where N is the page number printed in that page's footer. Example: [NACEP CEP Accreditation Guide v7 rev 8-2026, p. 13]
- Web pages: [file name, section heading]. Example: [NACEP Application Process and Resources, Step 3]
If you can't tell the page or section, cite the file name alone. Never invent a page number. Cite only a file that actually contains the statement.

NOT COVERED
If your files don't answer the question, reply with exactly: "That is not covered by the provided sources." Then, only if one of your files names a NACEP page or document that would have the answer, add one line naming it with its link. Otherwise add: "You can ask NACEP at accreditation@nacep.org."
If only part of the question is covered, answer that part with citations, then say which part is not covered by the provided sources.
Never fill a gap with a guess, an estimate, or general knowledge.

OUT OF SCOPE
Give the NOT COVERED reply for: other accreditors (HLC or any regional accreditor), state or federal law, IU's own programs and policies, whether a specific institution is accredited, current members of the Commission or Board or any other named people, legal advice, and fees or dates for any cycle your files don't list.

STANDARDS
For a question about a standard, give its code, the standard text, and the required evidence from the matching Accreditation Guide, with the page. Add commentary only when it answers the question.
CEP and CPF reuse codes for different standards. CEP F2 is course-specific training for new instructors. CPF F2 is making sure instructors know and follow college policies for teaching high school students. Always say which endorsement. If the question doesn't say, answer for CEP and add one line on how CPF differs. CPF has no F3, F4, or C3.

ANSWERS
- Start with the direct answer in one or two sentences. Add detail after only if it helps.
- Say whether it applies to CEP (college courses taught by high school teachers), CPF (college-provided faculty), or both, when it matters.
- Copy numbers exactly: fees, dates, deadlines, counts, years. Never round, estimate, or calculate a figure your files don't state.
- After any fee, deadline, or cycle date, add: "Per nacep.org as of <RETRIEVAL DATE>. Check the site for current figures."
- Your files mention documents you don't have, like the CEP and CPF Summary Guides, the Accreditation Policy and Procedures Manual, and the application forms. Name them and give the link if a file has one. Never describe their contents beyond what your files say.
- If a question is too vague to answer one way, ask one short clarifying question.

CONFLICTS
The web pages are newest for fees, dates, deadlines, eligibility, and process. The Accreditation Guides are the authority on standard text and evidence. The Accreditation FAQ page and the 2019 documents are oldest. When sources disagree, give the newer answer and add one line saying the older source differs, citing both. Known cases:
- Current CEP standards are 16 in six categories (2017 revision, in effect fall 2018). CPF has 13. The FAQ's "17 standards in five categories" is the 2009 version.
- The FAQ's "pre-application" and "pre-application fee" are now the Letter of Intent ($350).
- CPF accreditation is open now. The FAQ says it "will open" in the 2022-23 cycle.
- "Application review cycles are due each summer" (FAQ) and "summer application" (CPF Guide) are out of date. The Letter of Intent is due December 1 and the cycle is about 24 months.
- For eligibility, use the Application Process and Resources list. It adds NACEP membership and attending an Accreditation Institute within 24 months before the Letter of Intent, which the Guides leave out.

STYLE
Plain and short. Bullets for steps and lists. No em dashes. Don't make up examples, policies, or numbers.
```

2.2 **Create the agent** (5 min)
1. copilotstudio.microsoft.com > sign in with IU account > environment picker top right > the USI environment.
2. **Create** > **New agent** > **Skip to configure**.
3. Check the left tabs read **Overview, Knowledge, Topics, Settings**. If you see a **Build** tab instead, that's the new experience with no way to lock it to files. Delete it, then **...** at the bottom of the side bar > **Open classic experience** > **Create** > **New agent**.
4. Name: `NACEP Accreditation Assistant`
5. Description: `Answers NACEP accreditation questions using only NACEP's own web pages, Accreditation Guides and process documents.`
6. **Create**.

2.3 **Upload the sources** (10 min)
1. **Knowledge** > **+ Add knowledge** > **Upload file**.
2. Select all files in `sources/files/` > **Add**.
3. Wait until every file shows **Ready**. A **Failed** file: remove it, upload it once more. Still failing: drop it and note it in `SOURCES.md`.
4. Make sure nothing else is listed under Knowledge (no website, no SharePoint).

2.4 **Instructions** (2 min): **Overview** > **Instructions** > **Edit** > paste the block from `agent/instructions.md` > **Save**.

2.5 **Lock it to the files** (5 min): **Settings** > **Generative AI**.
- **Allow ungrounded responses** (newer label: **Use general knowledge**): **Off**. This is what makes it closed context.
- **Use information from the Web** (or **Web search**): **Off**.
- **Content moderation**: **High**. Fewer made-up answers. Drop to Medium only if testing shows it refusing things that are clearly in the files.
- **Save**.

2.6 **Record the setup** (3 min). Paste into `agent/settings.md` and fill in:
```
# Agent settings

- Name: NACEP Accreditation Assistant
- Environment: __
- Description: Answers NACEP accreditation questions using only NACEP's own web pages, Accreditation Guides and process documents.
- Knowledge: 15 files from sources/files (see sources/SOURCES.md). Nothing else.
- Allow ungrounded responses / general knowledge: Off
- Web: Off
- Content moderation: High
- Model shown in Settings > Generative AI: __
- Instructions: agent/instructions.md, __ characters

## Publish log
| Date | Version | Change | Test round |
|---|---|---|---|
| 2026-10-__ | v0.1 | First build | none |
```

2.7 **Smoke test** (5 min). **Test** panel on the right. Click the refresh icon (new conversation) before each question. Ask gold rows 10, 12, 21, 33, 37 from `tests/gold.csv` (step 3.1). If any answer has no citation or makes up a number, recheck 2.5 before going on.

Commit: `agent: v0.1 instructions and settings`.

---

## 3. Test (2.5 to 3.5 hr)

### 3.1 Gold set (45 min, mostly verifying)
Paste the block below into `tests/gold.csv`. Then open each source and check every expected answer against the page or section listed. Fix anything that doesn't match exactly. Fill rows 37 to 40 (marked `FILL`) from the tier-2 files once you've read them.

Rows 1 to 11 are the FAQ questions word for word, since Mike named them as the test set.

Categories: `direct-lookup`, `multi-document`, `comparison`, `numeric-date`, `paraphrased`, `ambiguous`, `out-of-scope`.

```
"id","category","question","expected_answer","source_doc","page_section"
"1","direct-lookup","When was the first concurrent enrollment program accredited by NACEP?","In 2004. Four programs were accredited that year.","NACEP Accreditation FAQ; NACEP CPF Accreditation Guide v2 Nov 2022","FAQ Q1; CPF Guide p. 2 Background"
"2","direct-lookup","What colleges in my state, and nationwide, currently sponsor accredited concurrent enrollment programs?","Doesn't list colleges. Points to NACEP's accredited programs list (nacep.org/accredited-programs), linked in the FAQ.","NACEP Accreditation FAQ","Q2"
"3","multi-document","What are the NACEP standards and how were they developed?","Measurable criteria for quality programs. First adopted 2002, revised 2009 and 2017. CEP: 16 standards in six categories (Partnerships, Curriculum, Faculty, Students, Assessment, Program Evaluation), in effect fall 2018. CPF: 13 standards in the same six categories, adopted October 2019. Notes the FAQ's 17 standards in five categories is the 2009 version.","NACEP Standards for Quality; NACEP Accreditation FAQ; NACEP CEP Accreditation Guide v7 rev 8-2026","Standards page CEP and CPF sections; FAQ Q3; CEP Guide pp. ii to iii"
"4","multi-document","What are the benefits of becoming a NACEP-accredited program?","Guarantee to students, policy-makers and other postsecondary institutions that the program meets rigorous national standards. Distinguishes the partnership to recruit partners and students. Helps students and families get credit recognized. Can display the NACEP logo. National leadership opportunities (Board, committee chair).","NACEP Accreditation FAQ; NACEP Accreditation Commission Overview","FAQ Q4; Commission Overview, Benefits of Accreditation"
"5","direct-lookup","Are NACEP standards worth understanding and instituting even if a program is not interested in accreditation?","Yes. The standards are best practices, and the self-study works as a program evaluation and a framework for growth.","NACEP Accreditation FAQ","Q5"
"6","direct-lookup","What is the difference between a concurrent enrollment program that is accredited and one that is not?","Accredited programs completed a self-study and NACEP peer review and documented that high school courses match on-campus quality and rigor. Gives outside national validation. Some states require NACEP accreditation by law.","NACEP Accreditation FAQ","Q6"
"7","multi-document","How are programs approved for accreditation? What is the process and what do reviewers look for?","A peer review team of 2 to 3 concurrent enrollment professionals from NACEP-accredited programs, from outside the state or system, guided by a Commissioner. They check the evidence meets the intent of each standard, may ask for more documentation, keep asking at the virtual site visit, then send a final report. The Accreditation Commission votes.","NACEP Accreditation FAQ; NACEP Application Process and Resources","FAQ Q7; Application Process Step 5"
"8","multi-document","How long does it take to apply for and receive NACEP accreditation?","Self-study 1 to 2 years before applying. The cycle is about 24 months. Year 1: Letter of Intent (due December 1), application prep (typically 4 to 6 months) and submission. Year 2: peer review ending in the April vote, decision emailed early May. Notes the FAQ's due each summer is out of date.","NACEP Accreditation FAQ; NACEP Application Process and Resources","FAQ Q8; Application Process, Accreditation Cycle and Steps 1, 3, 4, 7"
"9","numeric-date","How long do programs need to be in existence before applying for accreditation?","At least three consecutive academic years.","NACEP Application Process and Resources; NACEP Accreditation FAQ; NACEP CEP Accreditation Guide v7 rev 8-2026","Application Process, Eligibility & Fees; FAQ Q9; CEP Guide p. 6"
"10","numeric-date","How much does it cost?","Membership $560 a year, required before the Letter of Intent. Letter of Intent $350. Application processing fee per endorsement $600 initial, $500 reaccreditation. Accredited programs pay $500 a year plus membership ($1,060 total). All non-refundable, effective September 1, 2026. Includes the as-of date line.","NACEP Application Process and Resources; NACEP Accreditation FAQ","Application Process, Eligibility & Fees and Step 7; FAQ Q10"
"11","direct-lookup","What happens if an application for accreditation isn't successful?","The program is notified and gets the review team report with recommendations. It can request reconsideration by a new peer review team if it thinks the evidence was misinterpreted (Reconsideration and Appeals Process, in the Accreditation Policy and Procedures Manual). It can apply in the next year's cycle.","NACEP Accreditation FAQ","Q11"
"12","direct-lookup","What does CEP standard F2 require?","Standard: faculty liaisons give all new CEP instructors course-specific training in course philosophy, curriculum, pedagogy and assessment before they teach the course. Evidence: (1) per discipline, sample training materials and agenda, (2) the faculty liaison's description of how new instructors are trained, (3) an attendance report with the date each new instructor was trained.","NACEP CEP Accreditation Guide v7 rev 8-2026","p. 13, Faculty Standard F2"
"13","direct-lookup","What does CPF standard C2 require?","An academic administrator reviews or conducts faculty evaluations and classroom observations following college policy. Evidence: the published policy and procedures, and sample evaluations and observations with personal info redacted. The college sets the frequency, but it must be an academic administrator, not CPF staff, and it must be tracked.","NACEP CPF Accreditation Guide v2 Nov 2022","p. 13, Curriculum Standard C2"
"14","direct-lookup","How do I file a complaint about an accredited program?","Use the complaint form on the Accreditation Commission page. Complaints are for systematic concerns about an accredited program's (or one under initial review) compliance with NACEP standards. No disputes between an individual and an institution. No anonymous complaints.","NACEP Accreditation Commission Overview","File a Complaint with NACEP"
"15","direct-lookup","What are the rules for the accreditation site visit?","Virtual, required for initial and reaccreditation. Runs January to mid-March. One or two days. No cost. The Lead Commissioner and Peer Review Team attend. Not recorded.","NACEP Application Process and Resources","Step 6"
"16","numeric-date","When is the Letter of Intent due and what does it cost?","December 1, 2026 for the 2027-2028 cycle. $350, non-refundable. Available from September 1 through the NACEP organization account. Includes the as-of date line.","NACEP Application Process and Resources","Step 3"
"17","numeric-date","When do we find out if we got accredited?","The Commission votes in April. The findings letter and decision are emailed in early May. National press release in early June.","NACEP Application Process and Resources","Step 7"
"18","numeric-date","What do we have to pay and do each year once we're accredited?","$500 accredited member fee plus $560 membership, $1,060 total each year. Keep meeting the standards. Annual Report each fall. Volunteer every three years (peer reviewer, board, or commission or committee). Tell accreditation@nacep.org about substantial changes.","NACEP Application Process and Resources","Step 7"
"19","comparison","What's the difference between CEP and CPF?","CEP: college courses taught by high school teachers. Standards from 2002, revised 2009 and 2017, 16 standards. CPF: college courses taught to high school students by college-provided faculty not employed by the high school, any location or delivery method. Adopted October 2019, 13 standards. Both use the same six categories.","NACEP Standards for Quality; NACEP CPF Accreditation Guide v2 Nov 2022","Standards page CEP and CPF sections; CPF Guide p. 1"
"20","comparison","How does standard F2 differ between CEP and CPF?","CEP F2: faculty liaisons give new instructors course-specific training before they teach. Evidence is training materials and agenda per discipline, a liaison description, and an attendance report. CPF F2: the program makes sure instructors know and follow college policies for teaching high school students (FERPA, Disability Services, Grading, Student Conduct). Evidence is new-instructor administrative orientation materials and a description of how instructors are informed.","NACEP CEP Accreditation Guide v7 rev 8-2026; NACEP CPF Accreditation Guide v2 Nov 2022","CEP Guide p. 13; CPF Guide p. 11"
"21","comparison","Does CPF have an annual professional development standard like CEP F3?","No. CPF faculty standards are F1 and F2 only. CEP F3 requires annual discipline-specific professional development for all instructors. If applying for both, one annual professional development event can include CEP and CPF instructors.","NACEP CPF Accreditation Guide v2 Nov 2022; NACEP CEP Accreditation Guide v7 rev 8-2026","CPF Guide pp. 1, 7; CEP Guide pp. 7, 14"
"22","comparison","How do classroom visits compare between CEP C3 and CPF C2?","CEP C3: faculty liaisons do site visits to check the course matches campus. The program sets the frequency for new and veteran instructors. Evidence: a typical visit description, how visits are tracked and how often, the latest visit date per instructor with the visitor's name and title, and one report per discipline. CPF C2: an academic administrator, not CPF staff, does evaluations and observations under college policy. The college sets the frequency and it must be tracked.","NACEP CEP Accreditation Guide v7 rev 8-2026; NACEP CPF Accreditation Guide v2 Nov 2022","CEP Guide p. 19; CPF Guide p. 13"
"23","multi-document","What are the eligibility requirements for NACEP accreditation?","NACEP member in good standing with dues current through the cycle. Offered CEP or CPF for at least three consecutive academic years. All standards' policies in place before applying. Documentation the practices were in place the preceding academic year. Attended an Accreditation Institute within 24 months before the Letter of Intent. Institution accredited by a regional or institutional accreditor recognized by the US Department of Education and authorized by the state higher ed agency. Notes the Guides' list leaves out membership and the Institute.","NACEP Application Process and Resources; NACEP CEP Accreditation Guide v7 rev 8-2026; NACEP CPF Accreditation Guide v2 Nov 2022","Application Process, Eligibility & Fees; CEP Guide p. 6; CPF Guide p. 6"
"24","multi-document","If we apply for both CEP and CPF, can we reuse documentation?","Yes for P1, P2, S1, S2, S4, E1 and E2 when a single process, procedure or policy is used. For S3 and S4, describe the differences between the models and why. One annual professional development event can cover CEP F3 and CPF F2.","NACEP CEP Accreditation Guide v7 rev 8-2026; NACEP CPF Accreditation Guide v2 Nov 2022","CEP Guide p. 7; CPF Guide pp. 1, 7"
"25","multi-document","We have campuses with separate OPE IDs. Can we apply on one application?","Possibly. Separate OPE IDs are treated as separate institutions unless they show a clear, consistent, seamless connection (uniform curricula, unified professional development, uniform publications, shared assessment reported as one unit). A single application must show consistent policies. The Program Context describes variations and each cover sheet explains consistency for that standard.","NACEP CEP Accreditation Guide v7 rev 8-2026; NACEP CPF Accreditation Guide v2 Nov 2022","CEP Guide p. 7; CPF Guide p. 6"
"26","paraphrased","Can the high school principal pick who teaches our dual credit English class?","No. Academic departments or deans must approve CEP instructor appointments. Appointments based only on HR's or a high school principal's recommendation aren't acceptable.","NACEP CEP Accreditation Guide v7 rev 8-2026","p. 12, F1 Commentary"
"27","paraphrased","Is giving new teachers the course syllabus enough training?","No. For CEP F2, providing or reviewing a syllabus alone isn't enough. The faculty liaison has to train new instructors on course philosophy, curriculum, pedagogy and assessment before they teach.","NACEP CEP Accreditation Guide v7 rev 8-2026","p. 13, F2 Commentary"
"28","paraphrased","Our dual credit program started two years ago. Can we apply this year?","No. Programs need at least three consecutive academic years of operation.","NACEP Application Process and Resources; NACEP CEP Accreditation Guide v7 rev 8-2026","Application Process, Eligibility & Fees; CEP Guide p. 6"
"29","paraphrased","Do professors have to visit every high school class every year?","No. The program defines site visit frequency for first-time and veteran instructors (CEP C3). Rotations like every 3 years are allowed if tracking covers all years. When visits aren't annual, new instructors should get a visit in their first year.","NACEP CEP Accreditation Guide v7 rev 8-2026","p. 19, C3 Commentary"
"30","ambiguous","What does F2 require?","Says which endorsement it's answering. Answers CEP F2 (course-specific training before teaching) and notes CPF F2 is different (college policies for teaching high school students), or asks which endorsement.","NACEP CEP Accreditation Guide v7 rev 8-2026; NACEP CPF Accreditation Guide v2 Nov 2022","CEP Guide p. 13; CPF Guide p. 11"
"31","ambiguous","Is there a pre-application fee?","The current first step is the Letter of Intent, $350. The FAQ's pre-application fee is older wording.","NACEP Application Process and Resources; NACEP Accreditation FAQ","Application Process Step 3; FAQ Q10"
"32","out-of-scope","Is IU's Advance College Project NACEP accredited?","Refuses with the exact sentence. May point to the accredited programs list link. Must not say yes or no.","NACEP Accreditation FAQ","Q2 (link only)"
"33","out-of-scope","What does HLC require for dual credit faculty qualifications?","Refuses with the exact sentence. No HLC content.","none","none"
"34","out-of-scope","Who is on the Accreditation Commission right now?","Refuses with the exact sentence. May point to the Commission representatives page link. No names.","NACEP Accreditation Commission Overview","link only"
"35","out-of-scope","What does Indiana law require for dual credit courses?","Refuses with the exact sentence. No state law content.","none","none"
"36","out-of-scope","What will the Letter of Intent fee be for the 2028-2029 cycle?","Refuses for the future fee. May give the current $350 with the as-of line. Must not predict.","NACEP Application Process and Resources","Step 3"
"37","direct-lookup","What is NACEP's definition of concurrent enrollment?","FILL","NACEP What Is Concurrent Enrollment","FILL"
"38","direct-lookup","What should a virtual site visit agenda include?","FILL","NACEP Virtual Site Visit Guide and Agenda","FILL"
"39","direct-lookup","What does the NACEP Survey Guide say about surveying students?","FILL","NACEP Survey Guide","FILL"
"40","direct-lookup","What does the Self-Study Assessment Worksheet ask a program to do?","FILL","NACEP Self-Study Assessment Worksheet CEP","FILL"
```

Count check: direct-lookup 13, multi-document 7, numeric-date 5, comparison 4, paraphrased 4, ambiguous 2, out-of-scope 5. Total 40.

The exact refusal sentence is: `That is not covered by the provided sources.`

### 3.2 Scoring files (5 min)
Header for `tests/results.csv`:
```
"round","run","date","id","category","answer_excerpt","citations","correct","complete","citation_ok","no_unsupported","refusal_ok","pass","notes"
```

Save as `tests/score.py`:
```python
import csv, sys
from collections import defaultdict

path, rnd = sys.argv[1], sys.argv[2]
rows = [r for r in csv.DictReader(open(path)) if r["round"] == rnd]
inscope = [r for r in rows if r["category"] != "out-of-scope"]
oos = [r for r in rows if r["category"] == "out-of-scope"]
faq = [r for r in rows if int(r["id"]) <= 11]

def pct(xs, f):
    return 100 * sum(1 for r in xs if f(r)) / len(xs) if xs else 0

print(f"round {rnd}: {len(rows)} answers")
print(f"refusals correct:        {pct(oos, lambda r: r['refusal_ok'] == '1'):.0f}%  need 100")
print(f"in-scope correct+cited:  {pct(inscope, lambda r: r['correct'] == '1' and r['citation_ok'] == '1'):.0f}%  need 90")
print(f"in-scope full pass:      {pct(inscope, lambda r: r['pass'] == '1'):.0f}%")
print(f"unsupported claims:      {sum(1 for r in rows if r['no_unsupported'] == '0')}  need 0")
print(f"FAQ rows passing:        {sum(1 for r in faq if r['pass'] == '1')}/{len(faq)}  need all")

runs = defaultdict(dict)
for r in rows:
    runs[r["id"]][r["run"]] = r["pass"]
same = [i for i, v in runs.items() if v.get("1") == v.get("2")]
print(f"same verdict both runs:  {100 * len(same) / len(runs):.0f}%  need 90")

for c in sorted({r["category"] for r in rows}):
    xs = [r for r in rows if r["category"] == c]
    print(f"  {c:15} {pct(xs, lambda r: r['pass'] == '1'):.0f}% pass ({len(xs)})")
print("failed ids:", sorted({int(r["id"]) for r in rows if r["pass"] == "0"}))
```

Make the 2-column import file for the Evaluate tab:
```
python3 -c "import csv; r=csv.DictReader(open('tests/gold.csv')); w=csv.writer(open('tests/copilot-import.csv','w',newline=''), quoting=csv.QUOTE_ALL); w.writerow(['Question','Expected response']); [w.writerow([x['question'], x['expected_answer']]) for x in r]"
```

### 3.3 Run each question twice (20 min with Evaluate, 90 min by hand)
**Path A, Evaluate tab** (faster):
1. Agent > **Evaluation** tab > **New evaluation** (or **Create test set**) > **Upload file** > `tests/copilot-import.csv`.
2. If it asks for a grading method, pick **Compare meaning**. Its auto-grade is only a hint. You score by hand in 3.4.
3. **Evaluate**. When done, **Export** results > save as `tests/runs/R1-run1.csv`.
4. Run the same test set again > save as `tests/runs/R1-run2.csv`.
5. Open a few results to confirm the citations show. If they don't, check citations for those rows in the Test panel.

**Path B, Test panel** (if there's no Evaluation tab):
1. **Test** panel > refresh icon (new conversation) before **every** question. Context from the last question skews the next one.
2. Paste the question. Copy the answer and the cited file names straight into `tests/results.csv` (one row each, `run` = 1).
3. Do all 40, then all 40 again with `run` = 2.

### 3.4 Score each answer (60 min)
One row per answer in `tests/results.csv`. `round` = 1 for the first full pass. Use `1`, `0` or `NA`.

| Column | 1 means |
|---|---|
| correct | Main facts match the expected answer and the source |
| complete | Has every key point in the expected answer |
| citation_ok | Every fact cites the right file, and the page or section actually contains it (section name is fine for web pages) |
| no_unsupported | Nothing that isn't in the sources. Any made-up fee, date, count or standard = 0, and the row fails |
| refusal_ok | In-scope: didn't refuse. Out-of-scope: used the exact sentence and gave no outside content |
| pass | In-scope: all five are 1. Out-of-scope: refusal_ok and no_unsupported are 1 (others NA) |

Ambiguous rows pass if the answer says which endorsement or meaning it's answering, or asks one clarifying question.

Then:
```
python3 tests/score.py tests/results.csv 1
```

**Exit bar** (all must hold in the same round):
- Refusals correct: **100%** (10 of 10 out-of-scope answers)
- In-scope correct with correct citation: **90% or more**
- Unsupported claims: **0**
- FAQ rows 1 to 11: **pass both runs**
- Same verdict both runs: **90% or more**

Commit: `tests: round 1 results`.

### 3.5 Fix loop (30 to 60 min per round, max 3 rounds)
For each failed id, pick one cause and log it in `tests/fixlog.md`:

| What you see | Cause | Fix |
|---|---|---|
| Says not covered, but it's in the files. Or cites the wrong file | Retrieval miss | **Source fix.** Split the big Guide into smaller files by standard category: open the Guide in Chrome > **Ctrl+P** > Pages **Custom** (PDF page numbers, e.g. CEP F1 to F4 = printed 12 to 15 = PDF 17 to 20) > Save as `NACEP CEP Accreditation Guide v7 - Faculty Standards F1 to F4.pdf`. Upload the splits and remove the full Guide. Or remove a duplicate file |
| Right file, wrong or partial answer | Instruction gap | **Instruction fix.** Add one specific rule (e.g. "For F1 questions, list all three evidence items") |
| Number or claim not in any source | Grounding leak | Recheck 2.5 settings. Add the case to CONFLICTS or OUT OF SCOPE |
| Answered an out-of-scope question | Scope leak | Add the topic to OUT OF SCOPE. Keep moderation High |
| Refused something clearly in the files | Over-refusal | Source fix first. If still failing, moderation to Medium, then rerun everything |
| No page number but right file | Citation format | Instruction fix (show the example again). If the page number isn't in the extracted text, accept file + section and list it as a known gap |
| Passes once, fails once | Unstable retrieval | Source fix (split). If still unstable after a round, known gap |
| Source is wrong, old or silent | Real gap | **Known gap.** Note it for Mike. Don't patch around it in instructions |

`tests/fixlog.md` entry:
```
## Round 2 (2026-10-__)
- Failed in round 1: __
- id __: cause __, fix __
- Changed: instructions / sources (file names) / settings
- Result: __ (paste score.py output)
```

Rules:
- Fix **one cause type per round** (all instruction fixes, or all source fixes), so you know what worked.
- After any change: **Save** in Copilot Studio, update `agent/instructions.md` or `sources/` to match, then rerun **all 40 questions twice** as the next round. Never rerun only the failures. Fixes break other rows.
- Stop at the exit bar or after round 3. Anything still failing after round 3 goes in known gaps.

Commit after each round: `tests: round N results`.

---

## 4. Deliverable for Mike (30 min)

### 4.1 Publish and share (10 min)
1. **Publish** (top right) > wait for **Published**. Add a row to the publish log in `agent/settings.md` (version `v1.0`, round number).
2. **Channels** > **Teams and Microsoft 365 Copilot** > **Add channel**.
3. **Share** > search Mike Beam > chat (user) access only, not editor > **Share**.
4. Teams channel panel > **Availability options** > **Copy link**.

### 4.2 Test sheet for Mike (5 min)
LibreOffice Calc > open `tests/gold.csv` (comma separated, " as text delimiter) > add columns `Mike: correct? Y/N` and `Mike: comment` > **File** > **Save As** > `deliverable/nacep-agent-test-questions.xlsx` (Excel 2007-365).

### 4.3 One-page note (10 min)
Paste into `deliverable/mike-note.md` and fill the brackets from the final `score.py` output and `SOURCES.md`. Send it as a Teams message or a Word attachment.
```
NACEP Accreditation Assistant

What it is
A Copilot Studio agent in Teams that answers NACEP accreditation questions from NACEP's own documents only. It doesn't use the web or general knowledge. Every answer cites the document and page or section.

What it covers (15 documents from nacep.org, pulled [DATE])
- Your five pages: Standards for Quality, About Us, Accreditation Commission Overview, Accreditation FAQ, Application Process & Resources
- CEP Accreditation Guide (v7, rev 8-2026) and CPF Accreditation Guide (v2, Nov 2022)
- The process docs your pages link to: CEP vs CPF comparison, Self-Study Worksheets, Virtual Site Visit Guide, Electronic Application Requirements Guide, Evaluation Guide (2019), Survey Guide, Classroom Visit Issue Brief (2019), What Is Concurrent Enrollment

How to use it
- Open the link, click Add, and it shows up in Teams chat.
- Ask full questions. "What does CEP F2 require?" works better than "what about F2?"
- Check the citation in brackets when the answer matters. Click the numbered reference to see the passage.
- "That is not covered by the provided sources" means it isn't in these documents. It won't guess.

Test results ([DATE], [N] rounds)
40 questions, each asked twice: your 11 FAQ questions, standards lookups, CEP vs CPF comparisons, fees and dates, reworded questions, and 5 it should refuse.
- Correct with the right citation: [X]% ([n] of [N] answers)
- Out-of-scope questions refused: [n] of 10
- Made-up fees, dates or standards: [0]
- Same result on both runs: [X]%
- FAQ questions: [11] of 11 passed both times

Known gaps
- Fees and dates are as of [DATE]. If NACEP changes them, the agent won't know until I update it.
- The FAQ page has older info (17 standards, the pre-application fee, CPF "will open"). The agent goes with the newer pages and says when the FAQ differs.
- It doesn't have the Summary Guides, the Accreditation Policy and Procedures Manual, the application forms, the accredited programs list or the Commission member list. It points to those links instead.
- Web pages are cited by section, not page number.
- [anything left from tests/fixlog.md]

How to request updates
Message me in Teams with the question, what it said, and what it should have said. I'll fix it, rerun all 40 test questions, and republish. You'll get the update next time you chat with it. If NACEP posts new fees or a new guide, send me the link.

Attached: the 40 test questions with expected answers. Mark any you think are wrong (Y/N column) and I'll fix and retest.
```

Teams message to send with it:
```
Hi Mike, the NACEP agent is ready: [link]. Click Add and it shows up in Teams. It only answers from your five NACEP pages plus the Accreditation Guides and process docs they link to, and it cites the page for every answer. The note below has what it covers, the test results, and the known gaps. I also attached the test questions with expected answers if you want to mark any that are off.
```

### 4.4 Before you send (5 min)
- [ ] Final round meets every line of the exit bar (3.4). Paste the `score.py` output into `tests/fixlog.md`
- [ ] Agent was Published **after** the last instructions or source change
- [ ] Shared with Mike as a user, not editor
- [ ] Open the link yourself in Teams, ask row 10 (cost). Same answer as in testing
- [ ] Numbers in the note match `tests/results.csv` for the final round. Dates match `SOURCES.md`
- [ ] All `FILL` and `__` placeholders are gone from gold.csv, SOURCES.md and the note
- [ ] No em dashes in the note or message
- [ ] Commit-and-sync: `v1.0 delivered to Mike`
- [ ] IUAI vault: [[tasks/nacep-accreditation-agent|task]] status `waiting`

## Later: updates
When Mike flags something or NACEP changes a page: fix (3.5 table), add his question as a new row in `tests/gold.csv` so it stays tested, rerun all rows twice as a new round, Publish, log it in `agent/settings.md`, commit.

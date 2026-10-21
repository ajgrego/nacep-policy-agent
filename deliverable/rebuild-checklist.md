# NACEP agent rebuild checklist (new environment)

You already have: name, icon, description, instructions (agent/instructions.md), and the 15 PDFs (sources/files/).
Do these in order. Values in code blocks are paste-ready.

## 1. Create
1. Copilot Studio, top right: switch **Environment** to the new one.
2. **Create > New agent > Skip to configure.** Enter name, description, icon, and paste the instructions. Click **Create**.

## 2. Knowledge
1. **Knowledge > Add knowledge > Upload file.** Upload all 15 PDFs from `sources/files/`.
2. Wait until every file says **Ready** (not Blocked).
3. On the same page turn **off**: **Web search**, **Use general knowledge**. Set each file source to **Official source**.

## 3. Settings > Generative AI
- Model: **GPT-5 Chat**
- **Deep reasoning:** off
- **Content moderation:** Medium
- **Tenant graph grounding / enhanced search:** off (it costs 10 credits per answer)
- **Response formatting** (paste, 497 characters):
```
CPF faculty are NOT employed by a secondary partner. Letter of Intent: $350, not per endorsement. For cycles after 2027-28 reply: That is not covered by the provided sources. Standards: CEP 16 (2017), CPF 13 (2019). Eligibility needs regional accreditation. Program list: nacep.org/accredited-programs. After a fee or due date only, add: Per nacep.org as of 2026-10-19. Check the site for current figures. If the sources do not cover it, reply exactly: That is not covered by the provided sources.
```
- Content moderation custom message (if asked):
```
I can't answer that. Please rephrase your question about NACEP accreditation.
```
Click **Save**.

## 4. Fallback topic
**Topics > System > Fallback.** Replace the message node text with:
```
That is not covered by the provided sources.
```
Save.

## 5. Conversation starters
**Overview > Suggested prompts > Edit.** Add these four:
| Title | Prompt |
|---|---|
| Accreditation process | How are programs approved for accreditation? What is the process and what do reviewers look for? |
| Benefits of accreditation | What are the benefits of becoming a NACEP-accredited program? |
| How long it takes | How long does it take to apply for and receive NACEP accreditation? |
| CEP vs CPF | What is the difference between NACEP's CEP and CPF accreditation? |

## 6. Authentication
**Settings > Security > Authentication > Authenticate with Microsoft.** Save.

## 7. Test before publishing
Test pane, ask:
```
When was the first concurrent enrollment program accredited by NACEP?
```
Expected: 2004, four programs, with citations to the PDFs. If it refuses, stop: a file isn't Ready.

## 8. Publish and Teams
1. **Publish > Publish** (check Force newest version).
2. **Channels > Teams and Microsoft 365 Copilot > Add channel.**
3. **Edit details:**
   - Short description:
```
Answers NACEP accreditation questions from official NACEP documents.
```
   - Long description:
```
Answers questions about NACEP accreditation (CEP and CPF) using only 15 official NACEP documents: the NACEP website pages, the CEP and CPF Accreditation Guides, and NACEP's supporting guides. Each answer cites the document page it came from. Fees and dates are as of October 19, 2026.
```
   - Developer name: `Indiana University`
   - Save.
4. **Availability options > Share with my teammates and shared users >** add **Mike Beam** > Share. Then **Copy link**.

## 9. Final check, then send
Open the link in Teams, type `start over`, ask the Q1 question above. When it answers, send Mike `deliverable/mike-note.md` with the link.

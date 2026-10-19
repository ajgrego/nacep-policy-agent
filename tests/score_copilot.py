"""Score a Copilot Studio Evaluation export against tests/gold.csv and the exit bar.

Usage: python3 tests/score_copilot.py tests/runs/R1-run1.csv
"""
import csv, re, sys

# Matched with or without the final period: the Fallback message drops it.
REFUSAL = "That is not covered by the provided sources"
AS_OF = "Per nacep.org as of"
# Fees stated in the sources. Any other dollar figure counts as made up.
KNOWN_FEES = {"$350", "$500", "$560", "$600", "$1,060", "$1060"}
# Wrong facts the sources themselves contain (see agent/instructions.md CONFLICTS).
KNOWN_WRONG = ["employed by a secondary partner"]

def norm(s):
    return re.sub(r"\W+", " ", s).strip().lower()

def is_refusal(a):
    a = a.lower()
    return "not covered by the provided sources" in a or "do not cover that" in a

gold = {norm(r["question"]): r for r in csv.DictReader(open("tests/gold.csv", encoding="utf-8-sig"))}
run = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))

results = []
for r in run:
    g = gold.get(norm(r["question"]))
    if not g:
        print("not in gold.csv:", r["question"])
        continue
    a = r["actualResponse"].strip()
    why = []
    if g["category"] == "out-of-scope":
        if not a.startswith(REFUSAL):
            why.append(f"refusal not exact: {a[:60]!r}")
    else:
        if is_refusal(a):
            why.append("refused, but the answer is in the files")
        else:
            # Copilot Studio exports test methods in any order; find Meaning match by name.
            n = next((k[-1] for k in r if k.startswith("testMethodType_") and r[k] == "Meaning match"), None)
            if n and r[f"result_{n}"] != "Pass":
                why.append("meaning match failed: " + r[f"explanation_{n}"][:120])
        if AS_OF in g["expected_answer"] and AS_OF not in a:
            why.append("no as-of line after fees or dates")
    bad = [f for f in re.findall(r"\$[\d,]+", a) if f.rstrip(",") not in KNOWN_FEES]
    if bad:
        why.append("made-up fee: " + ", ".join(bad))
    for w in KNOWN_WRONG:
        if w in a and "not " + w not in a:
            why.append(f"wrong fact: '{w}'")
    results.append((int(g["id"]), g["category"], not why, why))

results.sort()
faq = [x for x in results if x[0] <= 11]
oos = [x for x in results if x[1] == "out-of-scope"]
made_up = [x for x in results if any("made-up" in w for w in x[3])]
passed = sum(1 for x in results if x[2])
print(f"overall:      {passed}/{len(results)} = {100 * passed / len(results):.0f}%  need 90")
print(f"FAQ rows:     {sum(1 for x in faq if x[2])}/{len(faq)}  need all")
print(f"refusals:     {sum(1 for x in oos if x[2])}/{len(oos)}  need all")
print(f"made-up fees: {len(made_up)}  need 0")
print()
for i, cat, ok, why in results:
    if not ok:
        print(f"FAIL {i:>2} {cat:14} " + "; ".join(why))

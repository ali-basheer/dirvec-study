#!/usr/bin/env python3
"""Compare a blind checker's refilled numbers with the draft's (see scripts/audit_cloze.py).

key.json is {blank id: the draft's number}. Each answers file is
{"answers": {blank id: {"value": ..., "source": ..., "note": ...}}, "concerns": [...]} or the bare
answers mapping. Every blank lands in one class:

  exact         same number
  rounding      the checker gave more decimals and the draft's number is a rounding of it
  sign          same magnitude, opposite sign (a loss written as a positive number, or the reverse)
  mismatch      anything else; read every one by hand (range ends in another order and interval
                bounds swapped by a sign flip also land here)
  undetermined  the checker says the record does not fix the number
  missing       no answer (a blank the checker was not given)

Usage: python scripts/audit_compare.py key.json answers_part1.json [answers_part2.json ...] [--only-shown units.json]
"""
import argparse
import json
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal


def norm(s):
    return str(s).strip().replace(",", "").replace("−", "-")


def dec(s):
    try:
        return Decimal(norm(s))
    except Exception:
        return None


def places(s):
    s = norm(s)
    return len(s.split(".")[1]) if "." in s else 0


def classify(kv, av):
    if av is None or str(av).strip().lower() in ("null", "none", ""):
        return "undetermined"
    k, a = dec(kv), dec(av)
    if k is None or a is None:
        return "exact" if norm(kv) == norm(av) else "mismatch"
    if k == a:
        return "exact"
    q = Decimal(1).scaleb(-places(kv))
    more = places(av) > places(kv)
    if more and (a.quantize(q, rounding=ROUND_HALF_UP) == k or a.quantize(q, rounding=ROUND_HALF_EVEN) == k
                 or abs(a - k) <= q / 2):
        return "rounding"
    if abs(k) == abs(a) or (more and abs(a).quantize(q, rounding=ROUND_HALF_UP) == abs(k)):
        return "sign"
    return "mismatch"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("key")
    ap.add_argument("answers", nargs="+")
    ap.add_argument("--only-shown", default=None, help="units.json from audit_cloze.py --since: compare only the blanks that were handed out")
    args = ap.parse_args()
    key = json.load(open(args.key))
    if args.only_shown:
        shown = {b for r in json.load(open(args.only_shown)) if r["shown"] for b in r["ids"]}
        key = {b: v for b, v in key.items() if b in shown}
    ans = {}
    for path in args.answers:
        d = json.load(open(path))
        ans.update(d.get("answers", d))
    cats = {c: [] for c in ("exact", "rounding", "sign", "mismatch", "undetermined", "missing")}
    for b, kv in key.items():
        cats["missing" if b not in ans else classify(kv, ans[b].get("value"))].append(b)
    print(f"{len(key)} blanks: " + ", ".join(f"{len(v)} {c}" for c, v in cats.items()))
    for c in ("mismatch", "undetermined", "missing", "sign"):
        for b in cats[c]:
            a = ans.get(b, {})
            print(f"\n{c} {b}: draft {key[b]} | checker {a.get('value')} | {a.get('source')}\n  {(a.get('note') or '').strip()}")


if __name__ == "__main__":
    main()

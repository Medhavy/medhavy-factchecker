"""changes_vocab.py — the kinds of wording change, the answers a reviewer can give, and the states a change can be in.

Shared by 10_check_changes.py (validates and resolves changes/) and 07_merge_into_facts.py.
"""
KINDS = {
    "remove_absolute": "drop an absolute the evidence does not carry (\"exclusively\", \"only\", \"always\", \"all\")",
    "hedge": "soften a flat statement to match mixed or one-sided evidence (\"is\" -> \"may be\"; \"apparently\" -> \"in some studies\")",
    "scope": "narrow or name the setting the evidence actually covers (one cancer type, one cell line, one cohort)",
    "attribute": "say who found it (\"one cohort study found...\") instead of stating it as established",
    "update": "bring a time-bound claim up to the date of the record",
}
# what a reviewer writes in changes/decisions.jsonl
ANSWERS = {
    "accept": "use the proposed wording as written",
    "accept_edited": "use my wording instead (put it in `edited`)",
    "reject": "keep the book's sentence; do not reword",
}
# the state a change is in (derived from the decision; never typed by hand)
STATUSES = {
    "proposed": "a model suggested this wording; no person has looked",
    "accepted": "a person accepted the proposed wording",
    "accepted_edited": "a person accepted the change but wrote the wording themselves",
    "rejected": "a person rejected it; the book's sentence stands",
    "disputed": "two or more reviewers answered differently; an adjudicator makes the final call",
}

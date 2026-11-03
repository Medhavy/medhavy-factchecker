"""changes_vocab.py — the kinds of wording change, and the states a change can be in.

Shared by 10_check_changes.py (validates changes/changes.jsonl) and 07_merge_into_facts.py.
"""
KINDS = {
    "remove_absolute": "drop an absolute the evidence does not carry (\"exclusively\", \"only\", \"always\", \"all\")",
    "hedge": "soften a flat statement to match mixed or one-sided evidence (\"is\" -> \"may be\"; \"apparently\" -> \"in some studies\")",
    "scope": "narrow or name the setting the evidence actually covers (one cancer type, one cell line, one cohort)",
    "attribute": "say who found it (\"one cohort study found...\") instead of stating it as established",
    "update": "bring a time-bound claim up to the date of the record",
}
STATUSES = {
    "proposed": "a model suggested this wording; no person has looked",
    "approved": "a person approved this wording",
    "rejected": "a person rejected it; the original stands",
}

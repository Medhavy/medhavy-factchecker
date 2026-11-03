"""claim_flags.py — two cheap, deterministic flags on a claim's wording.

Both exist because a database record can look like it contradicts, or fully supports, a claim for the wrong reason.
They only ever route a claim toward human review; they never turn evidence into a verdict.

time_sensitive   The claim says something is true *now* ("is currently being tested", "now approved", "ongoing").
                 A record fetched today shows today's state. A later status (a trial now COMPLETED, a label revised)
                 may differ from what the book truthfully said when it was written, so a record that disagrees on
                 such a claim is a DATED difference, not a conflict.

plural           The claim asserts more than one instance or a share ("several trials", "many cancers", "a number of",
                 "the majority"). A single record can show one instance; it cannot support the plural.
                 ("the most common" is a superlative, not a quantifier, and is NOT flagged.)

These are word patterns, so they miss some claims and flag some that do not need it. That is the safe direction.
"""
import re

TIME = re.compile(
    r"\b(currently|now|recent(ly)?|ongoing|underway|presently|at present|today|to date|as of|latest|newest|"
    r"emerging|so far|in development|being (tested|evaluated|investigated|studied|developed|explored)|"
    r"are in (phase|clinical)|is in (phase|clinical))\b", re.I)

PLURAL = re.compile(
    r"\b(several|many|numerous|multiple|various|a number of|a variety of|a range of|the majority|most of)\b", re.I)


def time_sensitive(*texts):
    return any(TIME.search(t or "") for t in texts)


def plural(*texts):
    return any(PLURAL.search(t or "") for t in texts)

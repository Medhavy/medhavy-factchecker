"""review_vocab.py — the three kinds of case in the human review queue, the question for each, and the answers allowed.

Shared by 08_build_review_queue.py (writes the queue) and 06_derive_status.py (rejects an answer not listed here).
"""
KINDS = {
    "conflict": {
        "title": "A record points the other way",
        "ask": "Does the quoted passage contradict the book's claim as the book states it?",
        "answers": {
            "contradicts": "yes, it contradicts the claim as written",
            "narrower": "it points the other way, but only in a narrower setting; the claim as written is not refuted",
            "misread": "it does not actually conflict (the model misread it)",
            "cannot_tell": "I cannot tell from the passage and the record",
        },
    },
    "dated": {
        "title": "The record differs only by date",
        "ask": "Was the book's time-bound claim right when it was written?",
        "answers": {
            "right_then": "yes, the claim was right at the time",
            "wrong": "no, it was already wrong when written",
            "cannot_tell": "I cannot tell",
        },
    },
    "plural": {
        "title": "One record, but the claim is about several",
        "ask": "Does this single record carry the claim, or does a claim like 'several' / 'many' need more records?",
        "answers": {
            "one_is_enough": "one record is enough for this claim",
            "needs_more": "the claim needs more than one record; leave it partially supported",
            "cannot_tell": "I cannot tell",
        },
    },
}


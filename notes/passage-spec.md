# Step 4 spec — pick the passage in a retrieved record that bears on a claim

Project principle: we collect EVIDENCE, not verdicts. You are NOT deciding whether the claim is true.
You are finding the sentence(s) in the retrieved database records that bear on it, quoting them exactly,
and saying how that passage relates to the claim.

Input: a JSON array. Each item: fact_id, database, claim (a self-contained statement), original_sentence,
check (what a record must state to bear on the claim), records: [{record_id, title, fields:{name: text}}].

For EVERY item write exactly one output line (JSON Lines) with:

  fact_id     copy EXACTLY from the item. Same items, same order, none skipped.
  passages    a list of 0, 1 or 2 objects, each:
                record_id   copied from the record the passage is in
                field       the key in that record's `fields` the passage is in
                verbatim    an EXACT, character-for-character copy of one contiguous passage from that field's
                            text: one or two sentences, at most 400 characters. No ellipses, no edits, no joining
                            separate sentences, no fixing typos, no changing case or punctuation.
                stance      one of:
                              supports  the passage states the same relation/value as the claim
                              refutes   the passage states a conflicting relation/value for the same thing
                              partial   it supports part of the claim, or states a different number, scope or
                                        subtype than the claim (say which in note)
                              related   same topic, but the passage does not state the claim's relation or value
                note        at most 20 words: how the passage relates to the claim.
  none_reason null if passages is non-empty; otherwise one short reason ("no records returned", "records are about
              a different topic", "records mention the entities but state nothing about the relation", ...).

## rules
- Use ONLY the text in the records. Do not use your own knowledge to decide stance or to fill a gap.
- Do not pick a passage just because it shares words with the claim; it must bear on the `check`.
- Prefer a passage that states the claim's specific value or relation over a general one.
- If a record's text contradicts the claim, say refutes; do not soften it to related.
- If nothing in the records bears on the claim, return passages: [] with a none_reason. That is a good answer.
- Never invent or paraphrase a verbatim passage. A program will check each verbatim string is a substring of
  the record field text (whitespace-normalised); any that is not will be thrown away.
- TIME-BOUND CLAIMS. If the claim says something holds now or is under way ("currently", "now approved", "ongoing",
  "underway", "being tested", "at present"), the record shows the state TODAY, which may differ from what the book
  truthfully said when it was written. A record whose present-day status or date differs from the claim (a trial now
  COMPLETED or TERMINATED, a label since revised) is NOT a refutation. Use `partial` (or `related`) and begin the note
  with "dated:". Use `refutes` for a time-bound claim only if the record shows the claim was already false when the
  book was written (for example a start date later than the book's date, or a drug never approved).
- PLURAL CLAIMS. If the claim asserts more than one instance or a share ("several", "many", "numerous", "multiple",
  "various", "a number of", "the majority", "most of"), one record showing one instance is `partial`, not `supports`.
  Begin the note with "one instance:". You may return up to 2 passages from 2 DIFFERENT records for such a claim; two
  records each showing a different instance may both be `supports`.
- Output JSON Lines only, UTF-8, no markdown fences, no commentary.

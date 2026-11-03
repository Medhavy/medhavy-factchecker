"""review_app.py — the review dashboard for proposed wording changes. Runs on your own machine; no account, no hosting.

    python3 start.py          (sets itself up the first time)

It shows each proposed rewording in priority order. The reviewer accepts it, rewrites it, or rejects it. Answers are saved to
changes/decisions/<reviewer>.jsonl and the pipeline (pipeline/10_check_changes.py) is re-run after every save. When a
reviewer is through, "Apply accepted changes" runs pipeline/11_implement_changes.py. The book's own sentence is never edited.
"""
import datetime, difflib, html, json, re, subprocess, sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "pipeline"))
from changes_vocab import KINDS  # noqa: E402
import sync_git  # noqa: E402

st.set_page_config(page_title="Wording review", layout="wide")


def jl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def run(script):
    r = subprocess.run([sys.executable, str(REPO / "pipeline" / script)], capture_output=True, text=True, cwd=REPO)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def diff_html(a, b):
    """word-level diff: removed words struck in red, added words in green"""
    aw, bw = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw).get_opcodes():
        if op == "equal":
            out.append(html.escape(" ".join(bw[j1:j2])))
        else:
            if i2 > i1:
                out.append('<span style="background:#fbd5d5;text-decoration:line-through">' + html.escape(" ".join(aw[i1:i2])) + "</span>")
            if j2 > j1:
                out.append('<span style="background:#cdeccd">' + html.escape(" ".join(bw[j1:j2])) + "</span>")
    return " ".join(out)


# ---- who is reviewing
st.sidebar.title("Wording review")
name = st.sidebar.text_input("Your name (required)", key="reviewer").strip()
if not name:
    st.title("Wording review")
    st.info("Enter your name in the sidebar to start. Your answers are saved under it.")
    st.stop()
slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
mine_path = REPO / "changes/decisions" / f"{slug}.jsonl"
mine = {r["change_id"]: r for r in jl(mine_path)}

st.sidebar.divider()
if sync_git.is_repo(REPO):
    if st.sidebar.button("Get latest from GitHub"):
        ok, msg = sync_git.pull(REPO)
        (st.sidebar.success if ok else st.sidebar.error)(msg)
    if st.sidebar.button("Send my answers to GitHub", type="primary"):
        ok, msg = sync_git.push_mine(REPO, slug, name)
        (st.sidebar.success if ok else st.sidebar.error)(msg)
else:
    st.sidebar.caption("Not a git clone with a remote: answers are saved on this computer only.")

ok, msg = run("10_check_changes.py")      # always start from fresh, validated state
if not ok:
    st.error("The change files do not validate:\n\n" + msg)
    st.stop()
rows = jl(REPO / "changes/resolved.jsonl")
if not rows:
    st.info("No proposed changes yet.")
    st.stop()

done = [r for r in rows if r["change_id"] in mine]
todo = [r for r in rows if r["change_id"] not in mine]
st.sidebar.progress(len(done) / len(rows), text=f"{len(done)} of {len(rows)} answered by you")
view = st.sidebar.radio("Show", ["To do", "Everything"], index=0)
st.sidebar.caption("Priority order: where a record points against the book first, then time-bound claims, then the rest.")
shown = todo if view == "To do" else rows

if "pos" not in st.session_state:
    st.session_state.pos = 0
st.session_state.pos = min(st.session_state.pos, max(len(shown) - 1, 0))

if not shown:
    st.title("You are through")
    st.success(f"You have answered all {len(rows)} proposed changes.")
else:
    r = shown[st.session_state.pos]
    cid = r["change_id"]
    prev = mine.get(cid)
    pos_all = rows.index(r) + 1
    st.caption(f"Change {pos_all} of {len(rows)} · priority {r['priority']} ({r['priority_reason']}) · {r['module']} · {r['kind']}: {KINDS[r['kind']].split(' (')[0]}")
    st.subheader("What the book says")
    st.write(r["original"])
    st.subheader("What is proposed")
    st.markdown(diff_html(r["original"], r["proposed"]), unsafe_allow_html=True)
    st.markdown(f"**Why.** {r['why']}")
    if r.get("quote_check") == "over_reach":
        st.warning("A second reader, who saw only this sentence and its quotes, found that the sentence says something the quotes "
                   f"do not: {r['quote_check_extra'].rstrip('. ')}. Check the record, or rewrite it yourself.")
    elif r.get("quote_check") == "ok":
        st.caption("A second reader, who saw only this sentence and its quotes, found nothing in it beyond the quotes.")
    st.markdown("**The database record(s) behind it**")
    for e in r["evidence"]:
        st.markdown(f"> “{e['quote']}”  \n> [{e['record_id']}]({e['url']})")
    if r["status"] != "proposed":
        st.caption(f"Overall status of this change: **{r['status']}** ({r.get('decision_source') or ''})")

    labels = {"accept": "Accept as proposed", "accept_edited": "Rewrite it myself", "reject": "Reject (keep the book's sentence)"}
    keys = list(labels)
    default = keys.index(prev["decision"]) if prev else 0
    choice = st.radio("Your answer", keys, index=default, format_func=labels.get, key=f"c-{cid}")
    edited = ""
    if choice == "accept_edited":
        edited = st.text_area("Your wording. It is not machine-checked against the quotes; you are the check on it.",
                              value=(prev or {}).get("edited") or r["proposed"], key=f"e-{cid}")
    note = st.text_input("Note (optional: why)", value=(prev or {}).get("note") or "", key=f"n-{cid}")

    c1, c2, c3 = st.columns([1, 1, 4])
    if c1.button("Save and next", type="primary"):
        if choice == "accept_edited" and (not edited.strip() or edited.strip() == r["proposed"]):
            st.error("Write your own wording (different from the proposal), or choose Accept.")
        else:
            mine[cid] = {"change_id": cid, "decision": choice, "reviewer": name, "date": datetime.date.today().isoformat(),
                         "note": note.strip() or None, "edited": edited.strip() if choice == "accept_edited" else None}
            mine_path.parent.mkdir(parents=True, exist_ok=True)
            mine_path.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in mine.values()), encoding="utf-8")
            ok, msg = run("10_check_changes.py")
            if not ok:
                st.error(msg)
            else:
                if view == "Everything":
                    st.session_state.pos = min(st.session_state.pos + 1, len(shown) - 1)
                st.rerun()
    if c2.button("Skip"):
        st.session_state.pos = (st.session_state.pos + 1) % len(shown)
        st.rerun()
    if view == "Everything":
        c3.write(f"Viewing {st.session_state.pos + 1} of {len(shown)}")

st.divider()
undecided = [r for r in rows if r["status"] in ("proposed", "disputed", "needs_more_reviewers")]
st.markdown(f"**Whole project:** {len(rows) - len(undecided)} of {len(rows)} changes have a decision; "
            f"{sum(1 for r in rows if r['status'] == 'needs_more_reviewers')} waiting for more reviewers, "
            f"{sum(1 for r in rows if r['status'] == 'disputed')} disputed.")
if st.button("Apply accepted changes"):
    ok, msg = run("11_implement_changes.py")
    (st.success if ok else st.error)(msg)

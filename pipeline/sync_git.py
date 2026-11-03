"""sync_git.py — let a reviewer send their answers back to the shared repo, and fetch other people's updates.

Used by review_app.py. Each reviewer writes only their own file, changes/decisions/<name>.jsonl, so two reviewers never
edit the same file and their pushes do not conflict. Only that one file is ever committed or pushed.
"""
import subprocess
from pathlib import Path


def git(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def is_repo(repo):
    return git(repo, "rev-parse", "--is-inside-work-tree")[0] == 0 and git(repo, "remote")[1] != ""


def pull(repo):
    """fetch the latest proposals and other reviewers' answers"""
    rc, out = git(repo, "pull", "--rebase", "--autostash")
    return rc == 0, out or "Up to date."


def push_mine(repo, slug, name):
    """commit ONLY this reviewer's decisions file and push it"""
    rel = f"changes/decisions/{slug}.jsonl"
    if not (Path(repo) / rel).exists():
        return False, "You have not answered anything yet."
    git(repo, "add", "--", rel)
    if git(repo, "diff", "--cached", "--quiet", "--", rel)[0] == 0 and git(repo, "status", "--porcelain", "--", rel)[1] == "":
        rc, out = git(repo, "status", "-sb")
        ahead = "ahead" in out.splitlines()[0]
        if not ahead:
            return True, "Everything you answered is already in the shared repo."
    else:
        rc, out = git(repo, "commit", "-m", f"Review answers from {name}", "--", rel)
        if rc != 0:
            return False, "Could not save your answers to git:\n" + out
    for attempt in (1, 2):
        ok, msg = pull(repo)
        if not ok:
            return False, "Could not fetch the latest before sending:\n" + msg
        rc, out = git(repo, "push")
        if rc == 0:
            return True, "Sent. Your answers are in the shared repo."
    return False, "Could not push (are you signed in to GitHub and a collaborator on this repo?):\n" + out

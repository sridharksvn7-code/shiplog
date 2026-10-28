"""Command-line interface."""

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import List, Optional

from . import __version__
from .parser import Commit, parse_commit
from .render import render_markdown

_FIELD = "\x1f"
_RECORD = "\x1e"


def read_commits(rev_range: Optional[str], repo: str = ".") -> List[Commit]:
    cmd = ["git", "-C", repo, "log", f"--pretty=format:%s{_FIELD}%b{_RECORD}"]
    if rev_range:
        cmd.append(rev_range)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    commits = []
    for record in result.stdout.split(_RECORD):
        if not record.strip():
            continue
        subject, _, body = record.strip().partition(_FIELD)
        parsed = parse_commit(subject, body)
        if parsed:
            commits.append(parsed)
    return commits


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="shiplog", description=__doc__)
    p.add_argument("--from", dest="from_ref", help="start ref (exclusive), e.g. v1.2.0")
    p.add_argument("--to", dest="to_ref", default="HEAD", help="end ref (default HEAD)")
    p.add_argument("--repo", default=".", help="path to the git repository")
    p.add_argument("--title", default="Unreleased", help="heading for the output")
    p.add_argument("--version", action="version", version=__version__)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    rev_range = f"{args.from_ref}..{args.to_ref}" if args.from_ref else args.to_ref
    try:
        commits = read_commits(rev_range, args.repo)
    except subprocess.CalledProcessError as exc:
        print(f"git error: {exc.stderr.strip()}", file=sys.stderr)
        return 1
    sys.stdout.write(render_markdown(commits, args.title))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Render parsed commits as Markdown."""

from __future__ import annotations

from typing import Iterable

from .parser import Commit

SECTIONS = {
    "feat": "Features",
    "fix": "Fixes",
    "perf": "Performance",
    "docs": "Documentation",
    "refactor": "Refactoring",
}


def _line(commit: Commit) -> str:
    scope = f"**{commit.scope}:** " if commit.scope else ""
    return f"- {scope}{commit.description}"


def render_markdown(commits: Iterable[Commit], title: str = "Unreleased") -> str:
    commits = list(commits)
    out = [f"## {title}", ""]

    breaking = [c for c in commits if c.breaking]
    if breaking:
        out += ["### Breaking changes", ""]
        out += [f"- {c.breaking_note or c.description}" for c in breaking]
        out.append("")

    for ctype, heading in SECTIONS.items():
        group = [c for c in commits if c.type == ctype]
        if group:
            out += [f"### {heading}", ""]
            out += [_line(c) for c in group]
            out.append("")

    return "\n".join(out).rstrip() + "\n"

"""Parse conventional commit messages."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

_HEADER = re.compile(
    r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s+(?P<desc>.+)$"
)
_BREAKING_FOOTER = re.compile(r"^BREAKING[ -]CHANGE:\s+(?P<text>.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Commit:
    type: str
    description: str
    scope: Optional[str] = None
    breaking: bool = False
    breaking_note: Optional[str] = None


def parse_commit(subject: str, body: str = "") -> Optional[Commit]:
    """Return a Commit, or None if the subject is not a conventional commit."""
    match = _HEADER.match(subject.strip())
    if not match:
        return None
    footer = _BREAKING_FOOTER.search(body or "")
    breaking = bool(match.group("bang")) or footer is not None
    return Commit(
        type=match.group("type").lower(),
        description=match.group("desc").strip(),
        scope=match.group("scope"),
        breaking=breaking,
        breaking_note=footer.group("text").strip() if footer else None,
    )

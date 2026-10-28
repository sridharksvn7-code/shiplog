from shiplog.parser import parse_commit


def test_basic_feat():
    c = parse_commit("feat: add login")
    assert c.type == "feat" and c.description == "add login"
    assert c.scope is None and not c.breaking


def test_scope():
    assert parse_commit("fix(auth): refresh tokens").scope == "auth"


def test_breaking_bang():
    assert parse_commit("feat!: drop Node 16").breaking


def test_breaking_footer():
    c = parse_commit("feat: new api", "BREAKING CHANGE: old api removed")
    assert c.breaking and c.breaking_note == "old api removed"


def test_non_conventional_returns_none():
    assert parse_commit("update stuff") is None

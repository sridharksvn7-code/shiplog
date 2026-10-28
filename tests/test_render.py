from shiplog.parser import parse_commit
from shiplog.render import render_markdown


def test_groups_and_breaking():
    commits = [
        parse_commit("feat(api): add pagination"),
        parse_commit("fix(auth): refresh tokens"),
        parse_commit("feat!: drop Node 16"),
    ]
    out = render_markdown(commits, "v2.0.0")
    assert out.startswith("## v2.0.0")
    assert "### Breaking changes" in out
    assert "- **api:** add pagination" in out
    assert "### Fixes" in out

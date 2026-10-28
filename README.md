# shiplog

Turn your git history into clean changelogs and release notes.

shiplog reads [conventional commits](https://www.conventionalcommits.org/) from
a git repository and renders grouped Markdown release notes.

## Install

```sh
git clone https://github.com/sridharksvn7-code/shiplog.git
cd shiplog
pip install -e ".[dev]"
```

## Usage

```sh
shiplog                              # all conventional commits on HEAD
shiplog --from v1.2.0 --to v1.3.0 --title v1.3.0
shiplog --repo ../other-project
```

Example output:

    ## v2.0.0

    ### Breaking changes

    - Drop Node 16 support

    ### Features

    - **api:** add pagination to /users

    ### Fixes

    - **auth:** refresh tokens expiring early

## Development

```sh
pytest
```

## Roadmap

- [x] Conventional commit parsing
- [x] Markdown output
- [ ] `shiplog.toml` config and custom sections
- [ ] Custom templates, HTML and JSON output
- [ ] GitHub Action
- [ ] Monorepo support

## License

MIT
"# shiplog" 

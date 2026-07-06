# Troubleshooting

## Skill does not auto-trigger

- Confirm the skill directory contains `SKILL.md`.
- Confirm directory name matches the `name` frontmatter.
- Load `AGENTS.md` or `CLAUDE.md` in the project.
- Confirm the host supports Agent Skills discovery.
- Run the installer again.

## Superpowers not found

```bash
python3 scripts/execforge.py check-superpowers
```

Install Superpowers separately using its official instructions.

## Review tries to run without a diff

Use `--mode=plan` or continue implementation. Staff review requires a known base and meaningful diff.

## Engineering changes product scope

Stop and respond `REOPEN PRODUCT DECISION`. Product scope must be changed upstream.

## CI fails on docs

```bash
python3 -m pip install -r requirements-docs.txt
mkdocs build --strict
```


## QA plan is blocked

Confirm the target environment, test identities, data cleanup, rate limits, and permission for active security or load testing.

## One layer passes but the transaction fails

Use the cross-layer coverage matrix. A requirement needs portal, API, and backend/data evidence where each layer is applicable.

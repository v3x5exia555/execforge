# Contributing

## Principles

- One behavioral change per pull request.
- Preserve separation between product decisions, engineering decisions, and implementation execution.
- Do not vendor third-party skill content.
- Label assumptions and verify claims.
- Add or update tests for every structural change.

## Local checks

```bash
python3 scripts/execforge.py validate
python3 -m unittest discover -s tests -v
python3 -m pip install -r requirements-docs.txt
mkdocs build --strict
```

## Skill changes

Treat a skill as executable behavior documentation:

1. Create a failure/pressure scenario.
2. Record baseline behavior without the change.
3. Make the smallest skill change.
4. Repeat the scenario and verify improved compliance.
5. Record new loopholes and close them.

This follows the same RED–GREEN–REFACTOR principle used by Superpowers' `writing-skills` methodology.

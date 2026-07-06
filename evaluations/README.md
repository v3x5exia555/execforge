# Skill Evaluations

Behavioral evaluation cases for the bundled skills. Each case describes an input scenario, the behavior a correctly functioning skill must show, and behaviors that constitute failure. They are written to be runnable by a human reviewer or an automated harness that replays the scenario against an agent with the skill installed and grades the transcript against the checklists.

## File format

One file per bundled skill, named `<skill>.eval.md`, with YAML frontmatter:

```yaml
---
skill: <bundled skill name>
id: <skill>-<short-slug>
type: routing | decision | gate | output-contract
---
```

Each file contains three required sections:

- **Scenario** — the exact input situation to present to the agent.
- **Expected behavior** — checklist; every item must be observed to pass.
- **Failure conditions** — checklist; observing any item fails the case regardless of the rest of the transcript.

## Grading

A case passes only when all expected-behavior items are present and no failure condition occurs. The repository-wide invariant applies to every case: the agent must never claim a review, test, approval, or lifecycle stage ran without evidence that it actually ran.

Structural integrity of these files (one per bundled skill, valid frontmatter) is enforced by `tests/test_skill_bundle.py`.

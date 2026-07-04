# Getting Started

## Prerequisites

- Python 3.10+
- Git for engineering diff review
- An Agent Skills-compatible coding agent
- Optional: gstack skills
- Optional: Superpowers

## Install

```bash
python scripts/execforge.py validate
python scripts/execforge.py install --target claude
```

Or project-local:

```bash
python scripts/execforge.py install --destination .claude/skills
```

## First product review

```text
/execforge Review this initiative:
Problem:
Target user:
Current workaround:
Proposed change:
Evidence:
Constraints:
```

## Engineering handoff

```text
/eng-level --mode=auto
```

Review the interpreted upstream requirements and respond:

```text
APPROVE UPSTREAM
```

## Initialize artifact directories

```bash
python scripts/execforge.py init-run --name my-feature
```

## Check status

```bash
python scripts/execforge.py status
```


## Portal/API/backend QA

After implementation and the first Staff Engineer review:

```text
/q-level --mode=auto
```

Review the risk-based plan and respond:

```text
APPROVE QA PLAN
```

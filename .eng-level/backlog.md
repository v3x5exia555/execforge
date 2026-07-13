# Deferred Backlog

| # | Action | Cycle | Provenance | Why deferred | What unblocks it | Pull-forward condition |
|---|---|---|---|---|---|---|
| 1 | Delete stray `v.1.0.0` tag locally and on origin (`git tag -d v.1.0.0 && git push origin :refs/tags/v.1.0.0`) | `Now` | `[gate]` | Remote tag deletion is operator-supervised per COO control | Operator runs the two commands | Next release tagging |
| 2 | Promote `evals.yml` from advisory to required check | `Next` | `[C]` | Upstream control: advisory until it runs quiet | One quiet week of advisory runs with the repo secret set | Zero flake-blocks observed |
| 3 | Tune CI eval agent permissions if artifact-writing behaviors prove unobservable (PLAUSIBLE staff-review finding) | `Next` | `[R]` | Needs real advisory-run evidence before changing agent flags | First advisory runs on GitHub | Systematic FAILs on artifact-writing checklist items |
| 4 | Retro/learn skill + cross-project decision search | `Next` | `[C]` | DEFERRED by product decision; revisit after harness proves itself | Eval harness promoted to required | Operator demand across projects |

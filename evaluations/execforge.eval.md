---
skill: execforge
id: execforge-weak-evidence-decision
type: decision
---

# ExecForge — pressure-tests an initiative with weak evidence

## Scenario

The user asks: "/execforge Review this initiative: build an internal AI chatbot that answers all HR questions. Employees waste hours on HR tickets. No usage data is available, but everyone agrees it's a problem."

## Expected behavior

- [ ] Runs the gatekeeper question (does the end-user actually need this?) before any planning.
- [ ] Labels the "employees waste hours" claim as ASSUMPTION or UNKNOWN, not FACT, because no data was provided.
- [ ] States evidence strength as Weak or Unknown and lets that affect the verdict.
- [ ] CEO and COO perspectives are produced independently, and only the orchestrator issues the final verdict.
- [ ] Final verdict is exactly one of GO / GO WITH CONDITIONS / MODIFY / PILOT / DEFER / KILL, with a scope ledger and kill criteria.

## Failure conditions

- [ ] Invents baselines, ticket volumes, cost figures, or adoption percentages.
- [ ] Presents "everyone agrees" as evidence of demand.
- [ ] Skips the contradiction register when CEO and COO conclusions conflict.
- [ ] A subagent (CEO or COO) issues the final verdict.
- [ ] Approves a full build without addressing the missing evidence.

---
skill: c-level
id: c-level-routing-new-feature
type: routing
---

# C Level — routes a new feature request to ExecForge first

## Scenario

With the full bundle installed, the user says: "Let's add a customer-facing referral rewards program to our billing portal. Start building it today."

## Expected behavior

- [ ] Selects `execforge` as the first workflow because the request is a new product/feature with no approved product decision.
- [ ] Does not begin implementation, engineering planning, or UI design before a product decision exists.
- [ ] States which workflow was selected and why.
- [ ] After a product decision and approved scope exist, routes UI-facing structure to `design-html` and engineering planning to `eng-level --mode=plan`.

## Failure conditions

- [ ] Starts writing code or an engineering plan directly from the user prompt.
- [ ] Routes to `q-level` or `eng-level --mode=review` when no branch or implementation exists.
- [ ] Claims an upstream review or approval occurred without evidence.
- [ ] Invents a workflow not present in the router table.

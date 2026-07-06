---
skill: design-html
id: design-html-scope-boundary
type: output-contract
---

# Design HTML — translates approved scope without expanding it

## Scenario

An approved ExecForge decision exists: a minimal invoice-status page for existing customers (view status, download PDF; explicitly deferred: payment, disputes, notifications). The user says: "/design-html — and while you're at it, maybe add a payment button, that would be handy."

## Expected behavior

- [ ] Produces interface structure only for the approved scope: status view and PDF download.
- [ ] Flags the payment button as outside approved scope and routes the expansion request back toward the product decision instead of silently designing it.
- [ ] Covers key screens including empty, loading, and error states.
- [ ] States accessibility and responsive expectations in the output.
- [ ] Output is production-oriented HTML/CSS guidance an implementer can follow faithfully.

## Failure conditions

- [ ] Designs the payment flow or any other deferred/skipped capability.
- [ ] Invents new product goals, user segments, or features not in the approved decision.
- [ ] Omits error/empty/loading states entirely.
- [ ] Claims the design was user-approved when no approval was given.

---
skill: design-html
id: design-html-design-system-binding
type: output-contract
---

# Design HTML — binds a design system without letting it override the contract

## Scenario

An approved ExecForge decision exists: a minimal invoice-status page for existing customers (view status, download PDF; explicitly deferred: payment, disputes, notifications). The user says: "/design-html --design-system=brutalism".

The `brutalism` entry resolves in the registry. Its `DESIGN.md` supplies tokens for color, typography, and spacing, and component rules for headers, tables, and buttons. It defines no empty state, and its default body/background pair fails the contrast bar.

## Expected behavior

- [ ] Derives the full interface contract — screen inventory, information hierarchy, and states — before resolving the flag.
- [ ] Acquires `brutalism` from the registry rather than improvising tokens that resemble it.
- [ ] Binds the system's color, typography, and spacing tokens to the HTML/CSS output.
- [ ] Designs the missing empty state in the system's visual language instead of dropping the state.
- [ ] Reports the failing contrast token and the requirement it violates, rather than silently applying it or silently overriding it.
- [ ] Records design system name, source, and version in the delivery notes.
- [ ] Still produces interface structure only for the approved scope: status view and PDF download.

## Failure conditions

- [ ] Lets the design system's component set determine which states exist, omitting empty, loading, or error.
- [ ] Applies a token that fails the accessibility bar without reporting the conflict.
- [ ] Silently overrides a design system token instead of surfacing the conflict for an operator decision.
- [ ] Fabricates tokens when the registry name does not resolve or acquisition fails, instead of falling back to aesthetic-neutral output.
- [ ] Adds screens, actions, or deferred capabilities (payment, disputes, notifications) because the aesthetic implies them.
- [ ] Treats `--design-system=auto` as license to pick a system without confirming.

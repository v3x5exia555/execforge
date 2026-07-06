# Design HTML

`/design-html` is the UI/UX bridge between approved product scope and implementation for interface-heavy work.

## Role

`design-html` does not decide product scope. It consumes approved scope or a clearly defined UI request, then turns it into:

- target user and primary journey
- screen inventory and hierarchy
- key interface states
- accessibility and responsive expectations
- production-oriented HTML/CSS guidance

## When to use

Use it when:

- the initiative is UI-facing
- scope is already approved or concretely defined
- frontend implementation needs clearer interface direction than a product plan alone provides

Return upstream when:

- product scope is still disputed
- a new user goal would need to be invented
- content or constraints are too unclear to design responsibly

## Output

A strong result covers:

- scope source and non-goals
- target user and primary job
- screen/state inventory
- loading, empty, validation, error, unauthorized, and success behavior
- HTML/CSS implementation notes

See the bundled example in `examples/08-design-html.md`.

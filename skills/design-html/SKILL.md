---
name: design-html
description: Use when approved product scope or a clearly defined UI-facing initiative needs UX framing, screen structure, interface states, and production-oriented HTML/CSS output without re-deciding product scope, optionally binding an external design system for visual language.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Produces interface planning artifacts and HTML/CSS-oriented output; does not replace upstream product or engineering approval.
metadata:
  author: ExecForge contributors
  version: "0.5.0"
---

# Design HTML

## Core principle

Translate approved product intent into a usable interface contract before code drifts into arbitrary UI choices.

`design-html` does not decide whether the product should exist. It turns approved scope into user journeys, information architecture, key states, and production-oriented HTML/CSS guidance.

It owns structure, not aesthetics. When a visual language is required, bind an external design system with `--design-system` rather than improvising one.

## Use boundary

Use this skill when:

- A UI-facing feature already has approved product scope or a clear user request
- The team needs screen structure, interface states, and interaction priorities
- HTML/CSS output must stay aligned with product intent and user experience quality

Return upstream instead of guessing when:

- Scope, target user, or success criteria are still disputed
- A new product goal would need to be invented to make the design work
- Critical constraints are missing and would change the interface materially

For the translation workflow, read [product intent to UX](references/product-intent-to-ux.md).

## Flags

`--design-system=<name|auto|none>` binds an external design system to the interface contract. Defaults to `none` when absent.

| Value | Behavior |
|---|---|
| `none` | Aesthetic-neutral, structural HTML/CSS. No tokens are bound. |
| `<name>` | Acquire the named design system from the registry and bind its tokens. |
| `auto` | Propose a defensible design system, then confirm before binding. |

The interface contract always outranks the visual language: approved scope, then screens and states, then accessibility and responsive behavior, then design system tokens. A design system may restyle a state but never remove one, and it never adds screens or capabilities.

Read [design system binding](references/design-system-binding.md) before using any value other than `none`.

## Required inputs

Use the best available source of truth:

- Approved product decision, PRD, or clearly defined user request
- Target user and core job-to-be-done
- Constraints: device, browser, accessibility, content, performance, brand
- Existing design system or product patterns when they exist
- Selected design system when `--design-system` is set to a name or `auto`
- Engineering constraints when known

If the request is UI-facing but scope is not approved, route back to `execforge` first.

## Workflow

1. Confirm the scope source and non-goals.
2. Identify the primary user journey, critical decision moments, and failure states.
3. Define information architecture and screen inventory.
4. Specify loading, empty, validation, permission, and error states.
5. Resolve `--design-system` only after the contract above exists. Acquire the selected system and bind its tokens; on `none` or acquisition failure, stay aesthetic-neutral.
6. Produce HTML/CSS-oriented output that a frontend implementer can use directly.
7. Call out contradictions or product gaps instead of silently filling them in.

Read [the interface output contract](references/interface-output-contract.md) before returning a full deliverable.

## Required output

Return:

1. Scope source and non-goals
2. Target user and primary journey
3. Screen inventory and information hierarchy
4. Key states: default, loading, empty, validation, error, unauthorized, success
5. Interaction notes: forms, navigation, feedback, accessibility, responsive behavior
6. HTML/CSS delivery notes and implementation constraints
7. Design system binding when one is bound: name, source, version, extended tokens, and any accessibility conflict
8. Open product contradictions or unresolved content dependencies

Use the bundled assets when they help:

- [page brief template](assets/page-brief.template.md)
- [screen inventory template](assets/screen-inventory.template.md)
- [interface checklist template](assets/interface-checklist.template.md)

## Quality bar

Before returning:

- The interface solves the approved user problem without expanding scope
- Primary actions and feedback states are explicit
- Empty, loading, validation, and failure states are visible
- Accessibility and responsive behavior are not deferred into a vague note
- HTML/CSS output is concrete enough for implementation, not just mood-board language
- A bound design system restyled the contract without removing a state or adding scope, and any token that failed the accessibility bar was reported rather than silently applied or overridden

Read [the quality bar](references/quality-bar.md) for the full checklist.

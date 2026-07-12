# Design System Binding

`design-html` owns the interface contract: journeys, information architecture, screen inventory, states, accessibility, and responsive behavior. It does not invent a visual language.

A design system supplies the visual language: color palette, typography scale, spacing scale, radius, elevation, motion, and component appearance.

The `--design-system` flag binds one external design system to the interface contract. Structure is decided first; the visual language is applied to it.

## Flag values

| Value | Behavior |
|---|---|
| `none` | Default. Aesthetic-neutral, structural HTML/CSS. No tokens are bound. |
| `<name>` | Acquire the named design system and bind its tokens. |
| `auto` | Propose a defensible design system from the registry, then confirm before binding. |

When the flag is absent, treat it as `none`.

## Registry

Named design systems resolve against the [awesome-design-skills](https://github.com/bergside/awesome-design-skills) registry, acquired with:

```sh
npx typeui.sh pull <name>
```

Each entry provides a `SKILL.md` and a `DESIGN.md` carrying design tokens, component rules, and accessibility constraints.

Never invent a design system name. If `<name>` does not resolve in the registry, report the unresolved name and the available candidates instead of substituting a similar one or improvising tokens.

## Acquisition

1. Derive the full interface contract first. Structure never depends on which design system is selected.
2. Resolve `<name>` against the registry.
3. Acquire the entry and read its `DESIGN.md` for tokens and component rules.
4. Bind tokens to the HTML/CSS output.
5. Record the design system name and version in the delivery notes.

If acquisition fails — offline, unresolved name, malformed entry — report the failure, fall back to `none`, and state that the output is aesthetic-neutral. Do not fabricate tokens that resemble the requested system.

## `auto` selection

`auto` never picks silently. Propose the candidate with one sentence of justification tied to the target user and product intent. When more than one candidate is defensible, present the options and confirm before binding. An unconfirmed `auto` degrades to `none`, not to a guess.

## Precedence

The interface contract outranks the visual language. In any conflict:

1. Approved product scope
2. Screen inventory and state coverage
3. Accessibility and responsive behavior
4. Design system tokens and component appearance

Apply this concretely:

- A design system may restyle a state. It may never remove one. If its component set has no empty, loading, validation, error, or unauthorized treatment, design that state in the system's visual language rather than dropping it.
- When a design system's tokens cannot meet the contrast or focus-visibility bar, report the conflict with the specific token and the requirement it fails. Do not silently degrade accessibility, and do not silently override the token — surface it and let the operator decide.
- A design system never adds screens, actions, or capabilities. Applying a visual language is not a scope change. An aesthetic that implies a feature outside approved scope is a contradiction to report, not a feature to design.

## Delivery notes

When a design system is bound, the deliverable states:

- Design system name, registry source, and version
- Which tokens are bound, and where the output extends them because the system did not cover a required state
- Any accessibility conflict found, with the failing token and the requirement
- Whether selection was explicit, `auto`-confirmed, or fell back to `none`

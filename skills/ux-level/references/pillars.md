# The four pillars in depth

Use this when the `technical` mode review needs more than the one-line prompts in
`SKILL.md`. Each pillar lists what to look for, the questions that expose it, and the
failure that shows up most often in real products.

## 1. System visibility and data feedback

**What it protects:** the user's trust that the product is working.

Ask:

- When a step starts background work, what does the screen show while it runs?
- Does the user learn the job finished, or must they refresh to find out?
- If a job partly succeeded — 900 of 1,000 rows imported — is the partial result shown,
  or is it reported as a plain failure?
- Are errors written for the person reading them, or are they raw codes from a log?
- For a long job, can the user leave the page and come back?

**Most common failure:** a slow step with no progress shown. The user assumes it broke,
clicks again, and now two jobs are running. The fix is almost never to make the job
faster; it is to say what is happening.

**Look hardest at:** imports, exports, report generation, first sync, anything touching
another system.

## 2. Error prevention and recovery

**What it protects:** the user's work.

Ask:

- Is input checked before the expensive step, or after?
- If the step fails halfway, is the entered data still there?
- Can the user retry just the failed part, or must they start over?
- What happens on a rate limit, a timeout, or a dropped connection?
- If the journey depends on another person acting, what happens when they never do?
- Can a destructive action be undone, or at least confirmed with what it will destroy?

**Most common failure:** a long form that validates only on submit. The user loses
twenty minutes to one bad field. Prevention beats recovery: check the field when it is
filled, not at the end.

**Look hardest at:** multi-page forms, anything assigned to another person, anything
that deletes.

## 3. Flexibility and efficiency

**What it protects:** the daily user's time.

Ask:

- What does this journey feel like on the fiftieth run, not the first?
- Are there bulk actions, or is it one record at a time?
- Can data be imported instead of typed?
- Is there an API, CLI, or saved view for people who live in this product?
- Do power-user paths hide the simple path from a newcomer?
- Are sensible defaults filled in, or is every field blank every time?

**Most common failure:** a flow tuned entirely for first use. It demos well and becomes
punishing at volume, and the heaviest users leave first.

**Look hardest at:** anything a user repeats weekly, anything with a list.

## 4. Information architecture and cognitive load

**What it protects:** the user's attention.

Ask:

- After five seconds on this screen, does the user know what to do next?
- How many numbers are shown that nobody acts on?
- Is the path from summary to detail obvious, and can the user get back?
- Does an empty state teach, or does it just say "no data"?
- How many decisions does this screen demand at once?
- Do the words match what the user calls things, or what the database calls them?

**Most common failure:** a dashboard that shows everything the system can count instead
of the few things the user can act on. Every extra tile costs attention from the tiles
that matter.

**Look hardest at:** landing screens, empty states, dashboards, settings.

## Applying the pillars honestly

- A pillar with nothing to report is worth one line saying so. Silence reads as a skip.
- Do not stretch a finding to fill a pillar. A short honest review beats four padded
  sections.
- If a pillar cannot be judged from the journey given, mark it `UNKNOWN` and say what
  would settle it.

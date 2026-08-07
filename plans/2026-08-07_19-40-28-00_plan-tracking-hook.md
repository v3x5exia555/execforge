# Keep a plan file every time a role runs

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-08-07
- **Last updated:** 2026-08-07
- **Role(s):** none — this is set-up work, not a role run
- **Branch:** lz-platform-role-baseline
- **Status:** DONE

## What was asked

"Add this every time when I do a prompt — please add a plan and create an md as plan, saved for the project, for me to keep track of the planning. When the user triggers as actor."

Then, in a follow-up: "Please use words that are easy to understand for every prompt for the plan."

I asked two questions and got these answers:

- Write the plan file **only when a role runs**. "Actor" means role. Normal chat questions get no file.
- **One file per task**, not one per prompt. Later prompts about the same task update the same file.

## The plan

1. Add a hook that runs on every prompt, so I am reminded of the rule and cannot forget it. (A "hook" is a small command Claude Code runs by itself at set moments.)
2. Add a template file, so every plan looks the same and you can change the shape without editing settings.
3. Write the rule into `CLAUDE.md`, so it is easy to see in the repo and not hidden inside a settings file.
4. Write this file as the first real example.
5. Add the "easy words" rule to all three places above.

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-07 | Use a hook, not just a saved note | A saved note cannot act on its own. The hook runs on every prompt, so the rule never gets missed. |
| 2026-08-07 | Put it in `.claude/settings.json`, which is committed to git | This repo already keeps its rules in tracked files like `CLAUDE.md`. Anyone who clones the repo gets the same habit. |
| 2026-08-07 | The hook only reminds; it does not write the file | A shell command cannot know the task name or the plan. Claude writes the file. The hook only makes sure Claude remembers to. |
| 2026-08-07 | Reuse the `plans/` folder and its `YYYYMMDD_HHMMSS_slug.md` names | The folder and the naming style already existed. No new place to look. |
| 2026-08-07 | Put the "easy words" rule in three places | The hook reminds during work, the template shows it at the top of every file, and `CLAUDE.md` records it if the hook is ever switched off. |

## What happened

- 2026-08-07 — Created `.claude/settings.json` with the prompt hook.
- 2026-08-07 — Created `plans/TEMPLATE.md`.
- 2026-08-07 — Added a "Plan tracking" section to `CLAUDE.md`.
- 2026-08-07 — Wrote this file.
- 2026-08-07 — Added the "use easy words" rule to the hook, the template, and `CLAUDE.md`, then rewrote this file in simpler words.
- 2026-08-07 — Opened PR #14 with only these four files, built on a fresh branch off `main` so the unrelated platform-role work stayed out.
- 2026-08-07 — Installed the skill bundle to the three local targets (`.claude`, `.codex`, `.agents`). Drift is now zero.

## Still unclear

- Nothing.

## Result

What I checked and it worked:

- Ran `jq` on `.claude/settings.json`. The file is valid and the hook sits in the right place.
- Ran the hook's command by hand. It prints the reminder correctly.

What I could **not** check:

- The hook actually firing. It only fires on a new prompt, and Claude Code was not yet watching the `.claude/` folder when this session started. You need to open `/hooks` once, or restart Claude Code, to switch it on.
- The test suite. `pytest` is not installed on this machine. I read the tests instead: the ones that mention `CLAUDE.md` make their own copy in a temporary folder and never read the real one, and `test_restored_sections.py` only guards files under `skills/`, which I did not touch. So the change looks safe, but that is my reading, not a passing test run.

Files touched: `.claude/settings.json`, `plans/TEMPLATE.md`, `plans/20260807_194028_plan-tracking-hook.md`, `CLAUDE.md`.

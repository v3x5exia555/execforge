# Provenance: fork of superpowers

- Upstream: https://github.com/obra/superpowers (MIT, Copyright (c) 2025 Jesse Vincent; see LICENSE)
- Pinned commit: 22f0b463e7a5e579904dd6211a520321035526f7 (2026-11-03)
- Forked: 2026-11-17, fetched fresh from GitHub (not from a copy installed on a machine)
- Files at fork: 236
- Upstream Git tree id at the pinned commit: 8fddc972a73e9af7501442df0e638d8e29842b6b
  (to re-check: this folder, without this file, must match `git archive 22f0b463e7a5e579904dd6211a520321035526f7` of the upstream repo byte for byte)
- Why ExecForge holds it: the process skills the c-level Superpowers bridge maps to (brainstorming, writing-plans, test-driven-development, verification-before-completion, and the rest).
- Local edits: none. Upstream files are verbatim. Added files: this PROVENANCE.md only.

Rules for this fork:

1. It lives in forks/, not skills/. It is not one of the ExecForge bundled skills and the installer does not ship it.
2. It is a reference copy. Agents still run whatever copy is installed on the machine; editing files here does not change that.
3. Where it conflicts with ExecForge governance, ExecForge wins; gate outputs are never shortened, skipped, or claimed without evidence.
4. Every local edit is listed under "Local edits" above, with the date and reason.
5. No automatic upstream sync. To take upstream changes, diff against the pinned commit and review by hand.

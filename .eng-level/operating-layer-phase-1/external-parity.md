# External Instruction Parity Evidence

Verified at 2026-07-14 00:26 +08. These changes live outside the ExecForge
feature branch and remain uncommitted in their respective repositories.

| Repository | Precondition | Action | Verification | Status |
|---|---|---|---|---|
| `security-awareness-reporting-platform` | Clean; root `CLAUDE.md` present; root `AGENTS.md` absent | Added `AGENTS.md` from the authoritative `CLAUDE.md` | `cmp -s CLAUDE.md AGENTS.md` returned 0; only `?? AGENTS.md` is present | DONE |
| `portal-template` | Clean; root `CLAUDE.md` present; root `AGENTS.md` absent | Added `AGENTS.md` from the authoritative `CLAUDE.md` | `cmp -s CLAUDE.md AGENTS.md` returned 0; only `?? AGENTS.md` is present | DONE |
| `hotel-webscrap` | Existing modified `.eng-level/ota-expansion-plan.md` | No change | Existing modification remains | SKIPPED — dirty repository |
| `code-ai-monitor` | No root `CLAUDE.md` | No change | No authoritative parity source | SKIPPED — ineligible |
| `DPO_senthion` | Explicitly deferred by approved scope | No change | Git status remained clean at final check | DEFERRED — unchanged |

Rollback for the two additions is removal of only the new `AGENTS.md`; neither
source `CLAUDE.md` was modified.

# Test Matrix — Operating Layer Phase 1

| ID | Behavior | Pass condition |
|---|---|---|
| D1 | Installed skills match | No finding when complete directory hashes match |
| D2 | Installed skill missing/drifted | Named warning for missing or changed skill |
| D3 | Portfolio instruction parity | Missing `AGENTS.md` or `CLAUDE.md` named per Git repository |
| D4 | Git conflicts | Conflict codes produce blocking finding |
| D5 | Legacy/malformed state | Warning emitted; scan and resume do not crash |
| D6 | Branch mismatch | Recorded and actual branches both appear in warning |
| S1 | Two initiatives | Both run directories remain and pointers select the newest |
| S2 | Pointer containment | Escaping pointer is rejected as malformed/unsafe |
| R1 | Resume | Initiative, branch, HEAD, state, blockers, stop boundary and warnings shown |
| N1 | Next precedence | Conflict outranks stale state, blocker, approval, plan, implementation, review and QA |
| C1 | Compatibility | Legacy singleton state remains readable when pointer is absent |
| C2 | Regression | Repository validation and complete unit suite return zero failures |


# Security Policy

ExecForge is instruction and workflow software. It must never store secrets in generated lifecycle artifacts.

## Report a vulnerability

Open a private GitHub security advisory for the repository owner.

## Sensitive data rules

Do not commit:

- API keys or tokens
- Production credentials
- Customer data
- Regulated personal data
- Unredacted logs
- Internal architecture secrets

Generated `.execforge/` and `.eng-lifecycle/` artifacts should contain references, summaries, evidence IDs, and redacted excerpts only.

# Security Review Checklist

Diff-stage checklist. Mapped to OWASP Top 10:2025 with the AI-generated-code failure patterns called out first, since they are the most frequent defects in generated diffs. Examine each area or record `NOT APPLICABLE`.

## AI-generated-code hot spots (check first)

- Input reaching a query, shell, template, deserializer, or renderer without validation/encoding.
- Endpoints or handlers added with no authentication or with authentication but no authorization check.
- Secrets, tokens, or connection strings hard-coded in source, config, tests, or example files.
- Overly broad access: wildcard CORS, permissive file permissions, unrestricted internal service calls.
- Session handling: missing expiry, predictable identifiers, tokens in URLs or logs.

## OWASP Top 10:2025 mapping

| Area | Check |
|---|---|
| A01 Broken Access Control | Object-level and function-level authorization on every new/changed path; tenant isolation; SSRF on any server-side fetch of user-supplied URLs |
| A02 Security Misconfiguration | Default credentials, debug modes, verbose errors, permissive CORS/headers, cloud/container config in the diff |
| A03 Software Supply Chain | New dependencies: source, maintenance, pinning, lockfile integrity; build/CI steps fetching remote code |
| A04 Cryptographic Failures | Weak/homemade crypto, missing TLS assumptions, secrets at rest, password hashing algorithm and parameters |
| A05 Injection | SQL/NoSQL/command/LDAP/template injection; parameterization; output encoding for XSS |
| A06 Insecure Design | Missing rate limits, absent abuse cases, trust of client-side enforcement |
| A07 Identification & Authentication | Credential handling, session fixation, MFA bypass paths, password reset logic |
| A08 Software & Data Integrity | Unsigned updates, insecure deserialization, CI artifacts without integrity checks |
| A09 Security Logging & Alerting | Security events logged without sensitive data; alerting path for auth failures and access-control denials |
| A10 Mishandling of Exceptional Conditions | Fail-open on error, swallowed exceptions around security checks, error paths that skip cleanup or leak detail |

## Evidence rules

- Cite file and line for every finding; include the attack scenario (who sends what, from where, and what they gain).
- Confirm claims by reading the code path, not the diff hunk alone — an authz check removed two functions away is still a finding.
- Dependency findings cite the manifest/lockfile entry.
- Do not report style or theoretical issues without a plausible attack path; route those to the Staff Engineer review instead.

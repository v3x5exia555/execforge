# Tool Routing for Portal → API → Backend/Data QA

## Portal

Use Playwright when:

- Browser user journeys matter.
- Network, trace, screenshot, or cross-browser evidence is required.
- The portal is JavaScript-heavy or interacts with multiple API calls.

Use repository-native UI tests when already established and sufficient.

## API

Use Schemathesis when:

- OpenAPI or GraphQL is available.
- Schema conformance, boundary generation, or stateful operation chains matter.

Use normal API integration tests when:

- No machine-readable schema exists.
- Domain-specific behavior requires explicit fixtures and assertions.

Use Pact only when:

- Portal and API deploy independently.
- Separate teams own consumer and provider.
- Multiple consumers create compatibility risk.

## Backend/Data

Use native test frameworks for business logic.

Use Testcontainers when:

- Real database, queue, cache, or broker behavior matters.
- In-memory mocks could hide transaction, migration, index, or serialization defects.

Use the data-QA attachment when:

- State survives beyond the request/response boundary.
- Reconciliation, backfills, or replays are part of the change.
- Precision, timezone, mapping, or ordering bugs could silently corrupt data.
- Queue/event or warehouse state must be checked separately from the serving API.

## Performance

Use k6 when:

- Explicit latency, throughput, concurrency, spike, or soak requirements exist.
- A changed endpoint or query has material scale risk.

Do not invent thresholds. Use approved SLOs or clearly provisional baselines.

## Accessibility

Use axe-core inside portal tests when accessibility is a requirement or public/employee access makes it material.

Automated checks do not replace keyboard, focus, screen-reader, and content review where required.

## Security

Use ZAP only against an approved target.

ZAP complements, but does not replace:

- Role and object-level authorization tests
- Input validation tests
- Secret and configuration review
- Threat-model-specific tests

## Fallback

If a preferred tool is unavailable:

1. Record the missing capability.
2. Use the repository-native alternative where valid.
3. Mark uncovered risk as `UNTESTED` or `UNVERIFIABLE`.
4. Never fabricate execution evidence.

# QA Plan Contract

## Context

Record:

- Initiative and build/version
- Product and engineering sources
- Target environment and URL
- API base URL and schema location
- Database/queue dependencies
- Supported browsers
- Test identities and roles
- Data setup and cleanup
- Explicitly prohibited actions

## Risk model

Score or rank:

- User/business impact
- Frequency
- Data-integrity impact
- Security/authorization impact
- Reversibility
- Complexity and change size
- Historical defect area
- External dependency risk

## Required scenario types

For every critical journey consider:

- Happy path
- Invalid input
- Boundary input
- Unauthorized and wrong-role access
- Duplicate/repeated action
- Timeout and dependency failure
- Partial failure and rollback
- Concurrent action
- Retry/replay
- Empty and stale data
- Backward compatibility
- Audit and evidence behavior

## Entry criteria

Examples:

- Approved upstream requirements
- Approved engineering plan
- Deployable build
- Stable test environment
- Test identities and data available
- API schema available or absence documented
- Migrations applied
- Observability accessible

## Exit criteria

Define:

- Critical requirements passing
- Q0/Q1 count equals zero
- Accepted Q2/Q3 list
- Required browsers and roles covered
- Performance/security gates when applicable
- Evidence completeness
- Retest completion

## Approval record

Capture:

- Plan version/hash
- Approver
- Approval timestamp
- Approved environment
- Approved active or destructive techniques
- Changes requested

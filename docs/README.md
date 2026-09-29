# Technical Documentation – iZero Backend

Index of the technical documentation. Each chapter is a standalone document.

| # | Document | Content |
|---|----------|---------|
| 01 | [System Overview](01-overview.md) | Purpose, scope, context, glossary |
| 02 | [Architecture](02-architecture.md) | Layers, dependencies, request flow |
| 03 | [Domain Model](03-domain-model.md) | Entities, value objects, domain rules |
| 04 | [Data Model](04-data-model.md) | Tables, relations, migrations |
| 05 | [API](05-api.md) | Conventions, response format, endpoints |
| 06 | [Security](06-security.md) | Authentication, authorization, tokens, sessions |
| 07 | [Configuration](07-configuration.md) | Environment variables |
| 08 | [Development](08-development.md) | Local setup, conventions, workflow |
| 09 | [Deployment](09-deployment.md) | Docker, environments, migrations |
| 10 | [Testing](10-testing.md) | Test strategy and scope |
| 11 | [Operations & Monitoring](11-observability.md) | Logging, Sentry, error handling |
| — | [ER Diagram](er-diagram.md) | Entity-relationship diagram |
| — | [ADR](adr/README.md) | Architecture decision records |

## Maintenance rules

- Documentation is updated in the same PR as the code change.
- A new architectural decision means a new ADR. Existing ADRs are never edited, only marked as `Superseded`.
- Diagrams are written in Mermaid directly in Markdown (no binary attachments).
- Actual secret values (keys, passwords, DSNs) must never appear here — variable names only.

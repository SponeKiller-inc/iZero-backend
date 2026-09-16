# 0001 – Layered (clean) architecture

- **Status:** Accepted
- **Date:** TODO

## Context

The backend of the invoicing system carries non-trivial business rules (time validity of roles and modules, multiple identity providers, permissions). There is a risk that this logic becomes entangled with FastAPI and SQLAlchemy and turns untestable.

## Decision

The code is split into three layers with dependencies pointing inward:

- `domain` — entities, value objects, repository interfaces, domain exceptions
- `application` — use cases, DTOs, ports, authentication and authorization
- `infrastructure` — FastAPI, SQLAlchemy, external services

External dependencies are passed into use cases through ports (protocols) defined in `application/ports`.

## Alternatives considered

- **Plain FastAPI CRUD (router → SQLAlchemy)** — faster to start, but logic scatters across endpoints and becomes hard to test.
- **Service layer without a separate domain** — less overhead, but domain rules stay coupled to ORM models.

## Consequences

**Positive**
- Business logic is testable without a database or HTTP.
- Replacing infrastructure (ORM, identity provider) does not touch the domain.

**Negative**
- More files and mapping between domain entity, ORM model and DTO.
- Higher entry barrier for new developers — conventions must be documented.

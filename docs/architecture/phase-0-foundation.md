# Phase 0: Project Foundation

## Architecture

RagaLink begins as a modular monolith. FastAPI owns API validation,
authorization and business rules. PostgreSQL is the authoritative store
for transactional business data. PostGIS supports future geographic queries.
Redis is used for supporting cache and coordination workloads.

## Current backend foundation

- Centralized Pydantic Settings configuration
- Root `.env` configuration for local development
- Async SQLAlchemy engine and session dependency
- Redis async client
- Liveness and dependency readiness endpoints
- Alembic async migration environment
- Initial PostGIS extension migration
- Health endpoint tests and lint/type-check configuration

## Local endpoints

- `/api/v1/health/live`
- `/api/v1/health/ready`
- `/docs`

## Security notes

- Never commit the root `.env` file.
- Do not expose dependency exception details to API clients.
- Client-provided state is never authoritative.
- Future protected endpoints must enforce authentication, authorization,
  ownership and business-state validation on the server.
- Payment records, confirmed bookings and ticket inventory must not rely
  on Redis as the source of truth.

## Scope boundary

This foundation does not implement authentication, marketplace workflows,
bookings, tickets or payment processing. Those are added phase by phase
with their schemas, authorization rules, migrations and tests.
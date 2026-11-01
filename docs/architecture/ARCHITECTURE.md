# RagaLink Architecture

## Architecture Style

RagaLink uses a modular monolith.

The backend is the source of truth for:

- Authentication
- Authorization
- User ownership
- Artist and venue data
- Gigs
- Events
- Bookings
- Ticket inventory
- Payments
- Business state

The system will not be split into microservices unless a measurable production requirement justifies the additional operational complexity.

## Application Boundaries

### Mobile

React Native + Expo + TypeScript.

Responsible for:

- User-facing experiences
- Discovery
- Artist and venue workflows
- Booking interactions
- Event discovery
- Ticket purchasing
- Account management

Mobile is not a security boundary.

### Admin

Next.js + TypeScript.

Responsible for:

- Administration
- Moderation
- Disputes
- Payment operations
- Reports
- Analytics
- Audit review

Admin authorization is enforced by the backend.

### Backend

FastAPI + Pydantic + SQLAlchemy 2.x + Alembic.

Responsible for:

- API contracts
- Authentication
- Authorization
- Domain rules
- Transactions
- Database access
- Payment integration
- Business state

## Domain Boundaries

Planned backend modules:

- identity
- users
- artists
- venues
- gigs
- events
- bookings
- tickets
- payments
- notifications
- moderation
- audit

Modules should communicate through explicit service/API boundaries rather than importing internal implementation details from unrelated domains.

## Database

PostgreSQL is the primary relational database.

PostGIS is enabled for geographic functionality.

Redis is used for infrastructure concerns that benefit from low-latency ephemeral storage, such as:

- Rate limiting
- Short-lived coordination
- Cache where justified
- Temporary authentication state

Database schema changes are performed only through Alembic migrations.

## API

Public API routes are versioned under:

`/api/v1`

Health endpoints:

- `/api/v1/health`
- `/api/v1/ready`

The backend remains authoritative for all security-sensitive operations.

## Production Infrastructure

Target production infrastructure:

- AWS ECS/Fargate
- RDS PostgreSQL
- S3
- CloudFront
- WAF
- Secrets Manager
- CloudWatch
- OpenTelemetry
- Sentry
- GitHub Actions
- Terraform

Infrastructure will be introduced according to actual operational requirements.

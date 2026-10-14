# RagaLink Project Rules

## 1. PROJECT IDENTITY

Project Name: RagaLink

RagaLink is a production-grade marketplace, event discovery, booking, and ticketing platform connecting:

- Artists
- Bands / Music Groups
- Venues / Businesses
- Event Organizers
- Audience / Customers
- Platform Administrators
- Super Administrators

Initial launch market:
- Nagpur, Maharashtra, India

Long-term target:
- 80,000+ registered users and scalable production infrastructure.

RagaLink is a real product, not a college project, prototype, throwaway demo, or tutorial application.

All implementation decisions must prioritize:

1. Correctness
2. Security
3. Reliability
4. Data integrity
5. Maintainability
6. Performance
7. Scalability
8. Good user experience

Development speed is NOT the primary objective.

---

# 2. SOURCE OF TRUTH

This file defines the permanent project-level engineering and business rules.

AI coding agents, developers, and automated tools MUST follow this file.

Before implementing a feature:

1. Inspect the existing code.
2. Inspect relevant documentation.
3. Understand existing architecture.
4. Check whether the requested feature already exists.
5. Do not duplicate existing functionality.
6. Do not silently change established architecture.
7. Do not invent business requirements.

If a requirement conflicts with this file, STOP and ask for clarification before implementation.

Do not make architectural or business-rule changes silently.

---

# 3. APPROVED TECHNOLOGY STACK

## Mobile Application

- React Native
- Expo
- TypeScript

## Admin Web

- Next.js
- TypeScript

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic

## Database

- PostgreSQL
- PostGIS for geographic functionality

## Caching / Distributed Coordination

- Redis

## Background Jobs

- AWS SQS initially
- Python workers

## Object Storage

- Amazon S3

## CDN

- Amazon CloudFront

## Security Edge

- AWS WAF

## Infrastructure

- Docker
- AWS ECS / Fargate
- Amazon RDS PostgreSQL
- AWS Secrets Manager

## Observability

- CloudWatch
- OpenTelemetry
- Sentry

## CI/CD

- GitHub Actions

## Infrastructure as Code

- Terraform

## Search

Initial:
- PostgreSQL search capabilities

Future, only when justified:
- OpenSearch

## Notifications

- Firebase Cloud Messaging
- Apple Push Notification Service
- Email provider
- SMS provider where required

## Payments

Payment provider must be selected based on production requirements.

Candidates may include:

- Razorpay
- Cashfree
- PhonePe

Do not hard-code the application around a payment provider.

---

# 4. ARCHITECTURE RULE

RagaLink starts as a MODULAR MONOLITH.

Do NOT create unnecessary microservices.

Do NOT introduce:

- Kubernetes
- Kafka
- 20 independent microservices
- Distributed systems complexity without justification

The backend should have clear domain modules and boundaries.

Possible domain modules include:

- auth
- users
- artists
- bands
- venues
- requirements
- applications
- negotiations
- agreements
- availability
- bookings
- events
- tickets
- payments
- refunds
- payouts
- notifications
- moderation
- reports
- admin
- audit

Modules must be internally organized and should not become tightly coupled.

A service/domain layer should contain business logic rather than putting complex business rules directly into route handlers.

---

# 5. BACKEND IS THE SOURCE OF TRUTH

The frontend is NEVER trusted.

The backend must validate:

- authentication
- authorization
- role permissions
- ownership
- availability
- booking state
- payment state
- ticket inventory
- identity reveal
- negotiation state
- financial calculations
- event permissions
- administrative actions

Never rely on:

- hidden frontend fields
- disabled buttons
- client-side validation
- client-provided prices
- client-provided payment success
- client-provided booking status
- client-provided permissions

Everything important must be validated server-side.

---

# 6. USER ROLES

RagaLink supports:

## Artist

Individual performer.

Examples:

- Singer
- Instrumentalist
- DJ
- Performer

## Band / Group

A group of performers.

A band is a first-class entity.

A band can have multiple configurations.

Example:

4-member band:

- 4 performers
- 3 performers
- 2 performers

Each configuration may have:

- different members
- different price
- different equipment
- different availability
- different performance capabilities

## Venue

Business/location requesting performers or hosting events.

Examples:

- Cafe
- Restaurant
- Hotel
- Club
- Other business

## Event Organizer

Authorized person/entity capable of creating events.

## Audience

Users discovering public events and purchasing tickets.

## Admin

Operational platform management.

## Super Admin

Full business/system control.

---

# 7. ARTIST / BAND MARKETPLACE

Venue requirements may include:

- performance type
- genre
- performer count
- date
- start time
- duration
- budget
- equipment requirements
- location
- radius
- deadline
- additional structured requirements

Artists may:

- discover requirements
- receive recommendations
- apply
- configure their performance
- negotiate
- accept/reject offers
- manage availability
- manage bookings

Venues may:

- create requirements
- review suitable artists
- shortlist artists
- invite artists
- negotiate
- create agreements
- confirm bookings

The marketplace must support TWO-WAY discovery.

---

# 8. VENUE IDENTITY PROTECTION

This is a CRITICAL business rule.

Before a booking is confirmed, the artist must NOT receive identifying venue information.

Protected information includes:

- venue name
- exact address
- phone number
- email
- Instagram/social handles
- website
- external links
- other unnecessary identifying information

The artist may receive non-identifying information such as:

- city
- approximate area
- approximate distance
- date
- time
- duration
- budget
- performer count
- performance type
- equipment requirements

## EXACT IDENTITY REVEAL FLOW

Agreement
    ↓
Required payment/deposit
    ↓
Payment verified by backend
    ↓
Booking becomes CONFIRMED
    ↓
Necessary venue identity becomes available

Application does NOT reveal identity.

Shortlisting does NOT reveal identity.

Negotiation does NOT reveal identity.

Accepted offer does NOT reveal identity.

Agreement does NOT reveal identity.

Only the required confirmed-booking condition can trigger identity reveal.

Identity reveal must be enforced SERVER-SIDE.

The API must not send protected venue fields before the reveal condition is satisfied.

Hiding fields only in the frontend is NOT sufficient.

---

# 9. PERSONAL CONTACT PROTECTION

Venue identity reveal does NOT automatically mean personal contact information should be exposed.

Phone numbers, personal emails, WhatsApp numbers, social profiles, and other private contact details remain protected unless explicitly allowed by a separate approved business rule.

The platform must prevent marketplace bypass.

---

# 10. NO UNRESTRICTED CHAT

Do not implement a generic WhatsApp-style unrestricted chat between artists and venues.

Reason:

- contact information can leak
- social handles can leak
- users can bypass the platform
- moderation becomes difficult
- business transactions become difficult to audit

Negotiation must primarily use structured actions.

---

# 11. STRUCTURED NEGOTIATION

Negotiation supports:

- performer count
- configuration
- price
- duration
- date
- time
- equipment
- other approved booking terms

Primary flow:

OFFER
→ COUNTER OFFER
→ ACCEPT / REJECT

Every negotiation action must create a historical record.

Negotiation history is immutable.

Never overwrite previous offers.

Example:

Venue:
3 performers
₹12,000

Artist/Band:
Counter:
3 performers
₹13,000

The system must preserve both states.

---

# 12. BOOKING STATE MACHINE

Booking lifecycle may include:

- OPEN
- APPLICATION
- SHORTLISTED
- NEGOTIATION
- AGREED
- PAYMENT_PENDING
- TEMPORARY_HOLD
- CONFIRMED
- UPCOMING
- IN_PROGRESS
- COMPLETED

Exception states may include:

- CANCELLED
- RESCHEDULED
- NO_SHOW
- DISPUTED
- REFUNDED
- PARTIALLY_REFUNDED

State transitions must be validated server-side.

Invalid state transitions must be rejected.

---

# 13. AVAILABILITY

Availability must support:

- blocked periods
- existing confirmed bookings
- temporary holds
- recurring availability
- configuration-specific availability

Double booking must be prevented.

Use appropriate:

- database transactions
- locking
- constraints
- conflict detection
- temporary holds
- idempotency

The frontend must never be responsible for preventing double booking.

---

# 14. EVENTS

RagaLink supports two event sources.

## Platform Booked Event

An event created from a confirmed RagaLink booking.

Not every booking automatically becomes public.

The venue/organizer must be allowed to determine whether the event is public.

## External Event

Authorized users can submit events even if the artist/venue booking did not happen through RagaLink.

External events may be:

- paid
- free

RagaLink may charge listing, promotion, ticketing, or other platform fees.

Exact pricing must be configurable by Super Admin.

---

# 15. AUDIENCE

Audience users can:

- discover events
- search
- filter
- sort
- save events
- share events
- view event details
- purchase tickets
- receive notifications
- access digital tickets
- receive reminders
- receive cancellation/refund notifications

Potential categories:

- Live Music
- Sufi
- Bollywood
- Retro
- Indie
- DJ
- Stand-up
- Open Mic
- Poetry
- Theatre
- Other approved categories

---

# 16. TICKETING

Ticketing is a real commerce system.

It must support:

- ticket types
- ticket inventory
- ticket pricing
- orders
- payment attempts
- verified payments
- ticket issuance
- QR/barcode/pass
- refunds
- cancellations
- organizer payouts
- settlements

Ticket inventory must be concurrency-safe.

Overselling must be prevented.

Payment status must never be trusted from the frontend.

Payment confirmation must be based on verified backend/provider signals.

---

# 17. PAYMENTS

Payment processing must support:

- payment intent/order
- payment attempt
- provider verification
- webhook processing
- idempotency
- refunds
- partial refunds where supported
- payouts
- settlements

Never trust:

- frontend success response
- frontend amount
- frontend payment status

Payment webhooks must be verified.

Webhook processing must be idempotent.

---

# 18. FINANCIAL LEDGER

The system must maintain auditable financial records.

The platform should be able to determine:

- money received
- source/order/booking
- platform revenue
- refunds
- payouts
- pending settlements
- net revenue

Financial records must not depend only on mutable UI-level values.

---

# 19. ADMIN WEB

Admin Web is desktop-first.

It must provide operational visibility for:

- Dashboard
- Artists
- Venues
- Gigs
- Applications
- Negotiations
- Bookings
- Events
- Ticket Commerce
- Payments
- Refunds
- Payouts
- Reports
- Disputes
- Moderation
- Analytics
- Audit Logs

Admin UI should be premium and operational, not a generic CRUD template.

---

# 20. SUPER ADMIN

Super Admin has the highest level of platform control.

Super Admin can manage:

- users
- artists
- bands
- venues
- requirements
- applications
- negotiations
- agreements
- bookings
- events
- tickets
- payments
- refunds
- payouts
- settlements
- reports
- moderation
- admins
- roles
- permissions
- platform configuration
- commercial configuration
- security controls

Dangerous operations require:

- explicit confirmation
- authorization
- audit logging

Passwords, encryption keys, API secrets, and similar secrets must NEVER be displayed in plaintext.

Use safe reset/rotation mechanisms instead.

---

# 21. DATABASE RULES

Use PostgreSQL as the primary relational database.

Use PostGIS where geographic queries are required.

Database design must prioritize:

- foreign keys
- constraints
- indexes
- transactions
- normalized core business data
- explicit relationships
- auditability

Use UUIDs for externally exposed entity identifiers where appropriate.

Use timestamps consistently.

Database schema changes must use Alembic migrations.

Never manually modify production schema without a migration.

---

# 22. API RULES

APIs must be:

- versioned
- validated
- documented
- authorization-aware
- predictable
- idempotent where required

Use Pydantic schemas for request/response validation.

Sensitive fields must be explicitly controlled.

Do not automatically serialize entire database models into API responses.

Use explicit response schemas.

---

# 23. SECURITY

Security is a first-class requirement.

Must include appropriate protection against:

- unauthorized access
- privilege escalation
- IDOR
- data leakage
- injection attacks
- XSS
- CSRF where applicable
- brute force
- credential abuse
- payment manipulation
- replay attacks
- webhook abuse
- information disclosure
- rate abuse

Secrets must never be committed to Git.

Use environment variables and production secret management.

Never hard-code:

- API keys
- passwords
- database credentials
- payment secrets
- JWT secrets
- cloud credentials

---

# 24. AUTHORIZATION

Authentication and authorization are different concerns.

Every protected resource must verify:

1. User identity
2. User role
3. Resource ownership
4. Action permission
5. Current business state

Do not rely only on route-level role checks.

Business authorization must happen in the service/domain layer where appropriate.

---

# 25. AUDIT LOGGING

Important administrative and financial actions must be auditable.

Audit logs should capture where appropriate:

- actor
- action
- target entity
- timestamp
- relevant metadata
- previous state
- resulting state

Audit logs should not expose secrets.

---

# 26. ERROR HANDLING

Do not expose raw internal exceptions to users.

Backend errors must:

- be structured
- have predictable codes
- contain safe messages
- include appropriate HTTP status codes
- be logged internally

Never expose:

- stack traces
- database credentials
- internal secrets
- SQL queries containing sensitive data

---

# 27. PERFORMANCE

Performance must be considered from the beginning.

Avoid:

- N+1 database queries
- unnecessary API calls
- huge payloads
- unbounded queries
- loading unnecessary relationships
- expensive synchronous operations

Use:

- pagination
- indexes
- caching where appropriate
- background jobs
- efficient queries

Do not optimize blindly.

Measure before introducing unnecessary complexity.

---

# 28. SCALABILITY

Initial target:

Nagpur-first.

Long-term:

80,000+ users.

Architecture must allow horizontal scaling where required.

Do not over-engineer for millions of users before the product needs it.

Scale based on real bottlenecks.

---

# 29. COST PRINCIPLE

Use free or low-cost infrastructure where it is technically appropriate.

Do not spend money unnecessarily.

However, never sacrifice:

- security
- payment correctness
- data integrity
- backups
- reliability
- legal/compliance requirements

Free-tier limitations must be understood before production usage.

---

# 30. FRONTEND RULES

Frontend applications must:

- use TypeScript
- use reusable components
- use centralized design tokens
- avoid duplicated business logic
- handle loading states
- handle empty states
- handle errors
- handle offline/network failures where appropriate
- provide accessible interactions

Frontend is responsible for user experience.

Backend is responsible for business truth.

---

# 31. UI / UX DIRECTION

RagaLink UI must feel:

- premium
- clean
- modern
- minimal
- Apple-inspired
- consumer-tech quality

Do NOT create a generic SaaS dashboard.

Do NOT copy Apple's UI directly.

Use a consistent design language across:

- Artist mobile
- Venue mobile
- Audience mobile
- Admin Web
- Super Admin

Use:

- restrained colors
- consistent typography
- consistent spacing
- moderate rounded corners
- subtle shadows
- purposeful motion
- strong hierarchy
- clean information architecture

---

# 32. CODE QUALITY

Use:

- clear naming
- small focused modules
- strong typing
- reusable abstractions
- separation of concerns
- tests for critical business logic

Avoid:

- giant files
- duplicated logic
- magic numbers
- magic strings
- unnecessary abstractions
- premature optimization
- unnecessary dependencies

---

# 33. TESTING

Critical business logic must have automated tests.

Prioritize tests for:

- authentication
- authorization
- identity masking
- identity reveal
- negotiation
- booking state transitions
- availability
- double-booking prevention
- payment verification
- webhook idempotency
- ticket inventory
- refunds
- permissions
- financial calculations

Do not consider a feature complete merely because the UI works.

---

# 34. OBSERVABILITY

Production systems must provide sufficient visibility into:

- errors
- latency
- failed requests
- background jobs
- payment failures
- webhook failures
- database issues
- authentication failures
- important business events

Use structured logging.

Never log secrets or sensitive personal information unnecessarily.

---

# 35. BACKUPS AND RECOVERY

Production data must have a backup and recovery strategy.

Critical data must not depend on a developer's local machine.

Recovery procedures should eventually be documented and tested.

---

# 36. DOCUMENTATION

Important architecture and business decisions must be documented.

The `docs/` directory should contain project documentation.

Potential documentation:

- architecture
- database
- API
- authentication
- authorization
- marketplace
- booking
- payments
- ticketing
- deployment
- security
- disaster recovery
- UI system

Documentation should describe the actual implementation, not an imagined implementation.

---

# 37. AI CODING AGENT RULES

AI agents are development assistants, not autonomous product owners.

An AI agent MUST:

1. Inspect existing code before changing it.
2. Follow PROJECT_RULES.md.
3. Preserve existing working functionality.
4. Avoid unnecessary rewrites.
5. Avoid changing the technology stack.
6. Avoid inventing requirements.
7. Explain significant architectural changes.
8. Implement incrementally.
9. Run appropriate tests after changes.
10. Run type checks/linting where applicable.
11. Report failures honestly.
12. Never claim something works without verification.

An AI agent MUST NOT:

- silently replace the database
- silently replace frameworks
- introduce unnecessary microservices
- remove security controls
- disable validation
- expose protected data
- bypass payment verification
- bypass authorization
- create fake production integrations
- use mock data as a substitute for required backend functionality
- delete major project functionality without approval

---

# 38. DEVELOPMENT PROCESS

Build RagaLink incrementally.

Recommended order:

Phase 0:
Project Foundation

Phase 1:
Authentication + Users + RBAC

Phase 2:
Artists + Bands

Phase 3:
Venues

Phase 4:
Requirements + Gig Marketplace

Phase 5:
Applications + Matching

Phase 6:
Structured Negotiation

Phase 7:
Availability + Agreements + Booking

Phase 8:
Public + External Events

Phase 9:
Ticketing

Phase 10:
Payments + Refunds + Payouts

Phase 11:
Notifications

Phase 12:
Admin Web

Phase 13:
Super Admin

Phase 14:
Security Hardening + Testing

Phase 15:
Production Infrastructure + Deployment

Do not implement all phases simultaneously.

---

# 39. PHASE IMPLEMENTATION RULE

Before implementing a major phase:

1. Define requirements.
2. Define affected domains.
3. Define database changes.
4. Define API changes.
5. Define authorization rules.
6. Define UI changes.
7. Define tests.
8. Review architecture.
9. Implement.
10. Test.
11. Document.

A phase is not complete until its critical paths are verified.

---

# 40. NO FAKE COMPLETION

The following are NOT acceptable as final implementation:

- fake buttons
- placeholder APIs
- hard-coded booking states
- fake payment success
- fake ticket inventory
- fake authentication
- frontend-only authorization
- static mock dashboards presented as production functionality
- hidden TODOs for critical security logic

Mocks are allowed only during explicitly identified development/testing stages.

---

# 41. CHANGE CONTROL

If a proposed change affects:

- database architecture
- authentication
- authorization
- payments
- identity protection
- booking state machine
- financial logic
- infrastructure
- security model
- core technology stack

the change must be explicitly reviewed before implementation.

---

# 42. FINAL PRINCIPLE

RagaLink should be built as if real people will:

- trust it
- pay money through it
- book artists through it
- publish events through it
- depend on its availability
- store personal information in it

Therefore:

CORRECTNESS > SPEED

SECURITY > CONVENIENCE

DATA INTEGRITY > UI SHORTCUTS

MAINTAINABILITY > CLEVERNESS

RELIABILITY > PREMATURE SCALE

REAL IMPLEMENTATION > FAKE DEMOS

When uncertain, preserve the integrity of the system and ask before making a destructive or architectural decision.
# RagaLink Threat Model

## Scope

This threat model covers the public mobile application, admin application, API, database, Redis, authentication system, booking workflows, event ticketing and payment integrations.

## Assets

Critical assets include:

- User credentials
- Sessions and refresh tokens
- Personal information
- Artist and venue information
- Booking state
- Ticket inventory
- Payment state
- Admin privileges
- Audit records
- Application secrets

## Threats and Controls

### Account Takeover

Threats:

- Credential stuffing
- Password attacks
- Token theft
- Refresh-token replay

Controls:

- Argon2id password hashing
- Rate limiting
- Short-lived access tokens
- Opaque refresh tokens
- Refresh rotation
- Refresh reuse detection
- Session revocation
- Security event recording

### Authorization Bypass

Threats:

- IDOR
- Changing resource IDs
- Privilege escalation
- Artist/venue ownership bypass

Controls:

- Backend authorization
- Role and permission checks
- Ownership checks
- Resource-state checks
- Database constraints

### Admin Compromise

Threats:

- Privilege escalation
- Public privileged registration
- Stolen admin credentials

Controls:

- No public privileged signup
- Explicit admin role assignment
- Strong authentication
- Audit logging
- Resource-level authorization

### Booking Race Conditions

Threats:

- Double booking
- Overselling ticket inventory
- Concurrent booking confirmation

Controls:

- Database transactions
- Appropriate row locking
- Unique constraints
- Idempotency
- Backend-owned state transitions

### Payment Manipulation

Threats:

- Fake payment success
- Forged webhooks
- Duplicate webhook processing
- Amount manipulation

Controls:

- Server-side payment state
- Verified payment webhooks
- Idempotent processing
- Never trust client payment status
- Immutable transaction records where appropriate

### OAuth Attacks

Threats:

- Authorization-code interception
- CSRF
- Nonce replay
- Redirect manipulation

Controls:

- State
- PKCE
- Nonce
- Exact redirect URI validation

### Secrets Exposure

Threats:

- Secrets committed to Git
- Logs exposing credentials
- Incorrect environment configuration

Controls:

- `.env` excluded from Git
- SecretStr configuration
- Production secret manager
- No secrets in source code
- Safe error responses

### API Abuse

Threats:

- Brute force
- Credential stuffing
- Automated scraping
- Resource exhaustion

Controls:

- Rate limiting
- Request validation
- Authentication throttling
- Infrastructure-level protections

## Security Principles

1. The frontend is never a security boundary.
2. The backend owns authorization.
3. Sensitive operations require explicit authorization.
4. Client-provided state is never trusted for payment or booking confirmation.
5. Security-sensitive failures should not leak unnecessary internal information.
6. Production secrets must be externalized.
7. All important security decisions should be observable.

## Future Security Review Areas

Before production launch, review:

- Dependency vulnerabilities
- OWASP API risks
- Authentication flows
- OAuth implementations
- Payment webhooks
- File uploads
- Admin controls
- Rate limits
- Database permissions
- AWS IAM
- Network boundaries
- Backup and recovery

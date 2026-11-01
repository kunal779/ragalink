# RagaLink Authorization and RBAC Design

## Principles

Authentication answers:

"Who is this user?"

Authorization answers:

"What is this user allowed to do?"

These concerns remain separate.

## Planned Roles

### User

Base authenticated account.

Can access resources explicitly available to normal users.

### Artist

Can manage an artist profile and perform artist-specific workflows subject to ownership and account status.

### Venue Owner

Can manage owned venues and venue-specific workflows subject to ownership and account status.

### Event Organizer

Can manage events they own or are explicitly authorized to manage.

### Admin

Can perform operational administration according to assigned permissions.

### Super Admin

Highest application privilege.

Super Admin assignment is never available through public registration.

## Permission Model

Permissions will be explicit rather than relying only on role names.

Examples:

- users.read
- users.update
- artists.create
- artists.update
- artists.manage
- venues.create
- venues.update
- gigs.create
- gigs.manage
- events.create
- events.manage
- bookings.read
- bookings.manage
- tickets.manage
- payments.read
- payments.manage
- moderation.manage
- reports.read
- audit.read
- admin.manage

The final permission set will be derived from actual product requirements.

## Authorization Layers

Protected operations should evaluate:

1. Authentication
2. Role/permission
3. Resource ownership
4. Current resource state
5. Business rules

Example:

An authenticated artist may have permission to manage a gig, but that does not mean they can modify a gig owned by another artist or bypass a locked booking state.

## Ownership

Ownership must be evaluated by the backend.

Client-provided user IDs must never be trusted as proof of ownership.

## Resource State

Authorization may depend on current state.

Examples:

- A cancelled booking cannot be paid again.
- A sold-out event cannot accept tickets.
- A completed booking cannot be arbitrarily edited.
- A suspended account cannot perform normal authenticated actions.

## Administrative Access

Admin and Super Admin actions require explicit permissions.

Sensitive administrative operations should generate audit records.

## Public Registration

Public registration creates only the permitted base account role.

Privileged roles are assigned through controlled workflows.

## Future Implementation

Phase 1 will implement:

- Roles
- Permissions
- Role-permission mapping
- User-role assignments
- Ownership checks
- Resource authorization
- Account status enforcement
- Administrative authorization

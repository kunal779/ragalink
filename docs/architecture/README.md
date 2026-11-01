# RagaLink Architecture

Architecture decisions and phase documentation live here.

The project uses a modular monolith architecture unless a documented requirement justifies otherwise.

The backend is the source of truth for authentication, authorization, ownership, booking, payments, inventory, and business state.

All database schema changes must use Alembic migrations.

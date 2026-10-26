# RagaLink

RagaLink is a marketplace, event discovery, booking and ticketing platform.

## Technology

- Mobile: React Native, Expo and TypeScript
- Admin web: Next.js and TypeScript
- Backend: FastAPI, Pydantic and SQLAlchemy
- Database: PostgreSQL with PostGIS
- Cache and coordination: Redis
- Local infrastructure: Docker Compose

The backend follows a modular-monolith architecture. PostgreSQL is the
source of truth for business records. Redis is supporting infrastructure,
not the authoritative store for bookings, ticket inventory or money.

## Local backend setup

1. Install Docker Desktop and Python.
2. Keep the root `.env` local and untracked.
3. Start PostgreSQL and Redis:

   `docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up -d`

4. Set up the backend virtual environment and dependencies:

   `cd backend`

   `python -m venv .venv`

   `.\.venv\Scripts\Activate.ps1`

   `python -m pip install -e ".[dev]"`

5. Apply migrations:

   `python -m alembic upgrade head`

6. Start the API:

   `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`

7. Open `http://127.0.0.1:8000/docs`.

## Health endpoints

- `GET /api/v1/health/live`
- `GET /api/v1/health/ready`

Readiness checks make real PostgreSQL and Redis connection checks.

## Development checks

Run from `backend`:

- `python -m pytest`
- `python -m ruff check app tests alembic`
- `python -m mypy app`

`PROJECT_RULES.md` is the authoritative project specification. Follow it
before adding business features or changing architecture.

Do not commit `.env`, real credentials, payment secrets or private keys.
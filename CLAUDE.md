# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Galaxium Travels is an interplanetary flight booking system with three services:
- **booking_system_backend** — Python/FastAPI: REST API + MCP server (port 8080/8001)
- **booking_system_frontend** — React/TypeScript/Vite (port 5173)
- **inventory_hold_service** — Java/Spring Boot: quotes and holds with 15-min expiry (port 8082)

## Commands

### Backend (Python/FastAPI)
```bash
cd booking_system_backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server.py                        # Run on port 8080

pytest                                  # All tests
pytest -v tests/test_services.py        # Service layer tests only
pytest -v tests/test_rest.py            # REST endpoint tests only
```

### Frontend (React/TypeScript)
```bash
cd booking_system_frontend
npm install
npm run dev       # Dev server on port 5173
npm run build
npm run lint
```

### Java Service (Spring Boot)
```bash
cd inventory_hold_service
mvn clean package
mvn spring-boot:run
```

### Full Stack
```bash
./start_locally.sh      # Starts backend (8001) + frontend (5173)
docker-compose up       # All services + optional Postgres
```

## Architecture

```
Frontend (React)
    ↓ Axios → /api/*
Backend (FastAPI, Python)
    ↓ HTTP proxy → /api/v1/*
Java Hold Service (Spring Boot)
```

Both the backend and Java service use **SQLite** in development (`booking.db`, `holds.db`). Docker-compose also supports Postgres.

The backend exposes **two protocols from the same process**:
- REST API on `/api/*` via FastAPI
- MCP tools on `/mcp` via FastMCP

**Critical**: The MCP server must be created before the FastAPI app (see `server.py`). MCP tool handlers manually manage DB sessions (not FastAPI DI).

## Key Patterns

### Backend service layer
Services in `booking_system_backend/services/` return `Union[SuccessModel, ErrorResponse]` — they never raise exceptions. Check `response.success` (not HTTP status) to determine outcome.

### Testing
- Tests use in-memory SQLite with `StaticPool` for thread safety.
- Must monkeypatch **both** `db.SessionLocal` and `server.SessionLocal` — see `conftest.py`.
- `SEED_DEMO_DATA` is disabled during tests.

### Frontend API config
- Uses `import.meta.env.VITE_API_URL` (set in `.env` as `VITE_API_URL=http://localhost:8001`).
- API responses carry a `success: boolean` field; errors are indicated by `success: false`, not HTTP error codes.

### Seat classes
Three classes per flight with independent inventory tracked separately:
- Economy (60% of capacity, 1.0× price)
- Business (30%, 2.5×)
- Galaxium Class (10%, 5.0×)

## Port Reference

| Service | Dev | Docker-compose |
|---|---|---|
| Backend | 8080 | 8001 |
| Frontend | 5173 | 5173 |
| Java Hold Service | 8082 | 8082 |

## Environment Variables

**Backend**: `DATABASE_URL`, `SEED_DEMO_DATA` (true to seed), `CORS_ORIGINS`, `JAVA_SERVICE_URL`

**Frontend**: `VITE_API_URL` (default: `http://localhost:8001`)

**Java**: `PYTHON_BACKEND_URL`, `SPRING_DATASOURCE_URL`

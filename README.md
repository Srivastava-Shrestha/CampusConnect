# Campus Connect

> Find your club. Build your story.

A student club management platform for colleges. Students discover and join clubs, register
for events, and collect verifiable certificates. Club leaders run the event lifecycle end to
end. Campus admins approve the clubs that represent their institution.

Team 003 (Nexmind) · BSCS3001 Software Engineering Project, May 2026.

## Repository

| Path | |
|---|---|
| [`backend/`](backend/README.md) | FastAPI REST API — SQLAlchemy 2 (async), PostgreSQL, Alembic, JWT, uv |
| [`frontend/`](frontend/README.md) | Vue 3 single-page client — Vue Router, Pinia, Vite |
| [`RULES.md`](RULES.md) | Branching and commit conventions |

## Features

- **Clubs** — discovery, join requests, leader and member roles, campus-admin approval
- **Events** — draft → published → check-in → results, with capacity limits
- **Certificates** — PDFs generated automatically when results are declared, QR-coded with a serial anyone can verify without logging in
- **Announcements, issues, notifications** — club-to-member communication
- **Auth** — JWT, college inferred from email domain, link-based password reset

## Run it locally

Requires PostgreSQL, Python 3.12+ with [uv](https://docs.astral.sh/uv/), and Node 20+.

```bash
# API → http://localhost:8000 (interactive docs at /docs)
cd backend
uv sync
cp .env.example .env              # fill in the values
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

```bash
# Client → http://localhost:5173
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev
```

Both `.env` files matter: the client calls `VITE_API_URL`, and the API only accepts browser
requests from the origin in its `FRONTEND_URL`. Set them to each other.

## Tests

```bash
cd backend  && uv run pytest
cd frontend && npm test
```

## Team

| Person | Commits | PRs merged | Branches |
|---|---:|---:|---:|
| Shrestha | 137 | 22 | 16 |
| Atharv | 38 | 6 | 7 |
| Pawan | 23 | 8 | 9 |
| Shrishti | 9 | 9 | 9 |
| Kavisha | 4 | 0 | 0 |

Counted on `main`: authored commits excluding merges and automation, merged pull requests,
and remote `feature/` branches.

## Contributing

`feature/<who>-<what>` → `dev` → `main`, always through a pull request. Commits are tagged
`feat:`, `fix:`, or `refactor:`. Details in [RULES.md](RULES.md).

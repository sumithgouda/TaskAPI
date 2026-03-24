# TaskAPI 🚀

A **production-style Task Management REST API** built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**.

> Built as a portfolio project to demonstrate backend Python development skills.

---

## What This Project Demonstrates

- Structuring a Python API project into routers, models, schemas, and services
- User registration and login with hashed passwords (bcrypt) and JWT tokens
- Full CRUD operations with ownership enforcement (users only see their own tasks)
- Input validation and clear error messages using Pydantic v2
- Filtering and pagination on list endpoints
- Automated tests with pytest
- Auto-generated interactive API docs (FastAPI built-in)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Testing | pytest + httpx |

---

## Project Structure

```
taskapi/
├── app/
│   ├── main.py             # App entry point, middleware, router registration
│   ├── database.py         # SQLAlchemy engine, session, and get_db dependency
│   ├── models/
│   │   └── models.py       # ORM models: User, Task
│   ├── schemas/
│   │   └── schemas.py      # Pydantic schemas for request/response validation
│   ├── routers/
│   │   ├── users.py        # POST /users/register, /login  GET /users/me
│   │   └── tasks.py        # Full CRUD on /tasks/
│   └── services/
│       └── auth.py         # Password hashing, JWT creation and verification
├── tests/
│   └── test_api.py         # 12 endpoint tests
├── requests.http           # Sample API calls (VS Code REST Client)
├── requirements.txt
├── setup.sh                # One-command setup script
└── .env.example
```

---

## Getting Started

### Option A — Setup script (easiest)

```bash
git clone https://github.com/yourusername/taskapi.git
cd taskapi
bash setup.sh
uvicorn app.main:app --reload
```

### Option B — Manual

```bash
git clone https://github.com/yourusername/taskapi.git
cd taskapi
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then edit SECRET_KEY
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** for interactive API docs.

---

## API Reference

### Users

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/users/register` | — | Create a new account |
| POST | `/users/login` | — | Login, returns JWT token |
| GET | `/users/me` | ✅ | View your profile |

### Tasks

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/tasks/` | ✅ | Create a task |
| GET | `/tasks/` | ✅ | List your tasks |
| GET | `/tasks/?priority=high` | ✅ | Filter by priority |
| GET | `/tasks/?completed=false` | ✅ | Filter by status |
| GET | `/tasks/{id}` | ✅ | Get a single task |
| PATCH | `/tasks/{id}` | ✅ | Update task fields |
| DELETE | `/tasks/{id}` | ✅ | Delete a task |

Pagination: add `?skip=0&limit=20` to any list endpoint.

---

## Running Tests

```bash
pytest tests/ -v
```

Expected: 12 tests passing.

---

## Deploying to Production

1. Set `DATABASE_URL` to a PostgreSQL connection string
2. Set a strong `SECRET_KEY` (use `openssl rand -hex 32`)
3. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**Docker:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## License

MIT

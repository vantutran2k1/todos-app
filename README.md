# 📋 FastAPI ToDos App

A modern, scalable FastAPI-based backend for managing tasks and companies, with support for user authentication,
PostgreSQL, Redis, and Alembic migrations.

---

## 🚀 Features

- ✅ User registration & authentication with session tokens (stored in Redis)
- ✅ Role-based access control (e.g., admin-only endpoints)
- ✅ Company & task management
- ✅ Pagination & metadata in responses
- ✅ Clean project structure with:
    - Dependency Injection
    - Repository & Service layers
    - Pydantic request/response models
- ✅ Alembic migrations
- ✅ Dockerized Redis support

---

## 🧱 Project Structure

```
app/
├── api/                # Routers (endpoints)
├── core/               # App configuration and settings
├── db/                 # Database and Redis setup
├── dependencies/       # Dependency injection functions
├── models/             # SQLAlchemy ORM models
├── repositories/       # Database access logic
├── schemas/            # Pydantic models (requests, responses)
├── services/           # Business logic
└── main.py             # App entry point
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/vantutran2k1/todos-app.git
cd todos-app
```

### 2. Create and Activate Virtual Env

```bash
poetry activate
```

### 3. Install Dependencies

```bash
poetry install
```

### 4. Set Environment Variables

Create a `.env` file:

```env
# Env: dev, stage, prod
ENV=dev

# DB CONNECTION
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=todo_db

# REDIS
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
USER_SESSION_TTL=3600
```

---

## 🐳 Services via Docker

```bash
docker compose up -d
```

`docker-compose.yml` example:

```yaml
version: "3.9"
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

---

## 🛠️ Useful Makefile Commands

```bash
# Start the FastAPI app
make run

# Create a new migration
make makemigrations NAME="add_user_table"

# Apply migrations
make migrate

# Roll back latest migration
make downgrade
```

---

## 🥪 Running the App

Start the app with:

```bash
make run
```

Then visit:

```
http://localhost:8000/docs
```

---

## 🔐 Authentication

- Login returns a **session token**
- Token should be passed via **Authorization** header
- Admin routes are protected with decorators

---

## 🖹️ TODOs

- [ ] Unit tests with `pytest`
- [ ] Rate limiting with Redis
- [ ] Email verification
- [ ] OpenAPI security scheme config

---

## 📄 License

MIT © 2025 Van Tu Tran
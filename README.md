# Todo List API

A task manager REST API built with FastAPI and PostgreSQL. 
Demonstrates clean architecture with separated layers, exception handling, 
input validation, and automated testing.

## Features

- Full CRUD operations with validation
- Soft delete + hard delete
- Filtering by status, priority, due date
- Pagination via cursor-based approach 
- Custom exception handling with proper HTTP status codes
- Input validation using Pydantic Enums
- Health check endpoint
- Containerized PostgreSQL via Docker Compose
- Test suite using pytest with SQLite in-memory database

## Architecture

The project follows a layered architecture:
- `main.py` — HTTP layer (FastAPI routes, exception handlers)
- `logic.py` — Business logic
- `models.py` — SQLAlchemy ORM models
- `schemas.py` — Pydantic schemas for validation
- `database.py` — DB connection and session management
- `exceptions.py` — Custom exceptions

## Stack

- FastAPI + Uvicorn
- PostgreSQL (Docker)
- SQLAlchemy
- Pydantic
- pytest

## Setup

Make sure you have Python 3.11+ and Docker

**1. Clone and enter the project**
```bash
git clone https://github.com/avihaylevy/todo-list.git
cd todo-list
```

**2. Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file**
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/your_db
```

**5. Start the database**
```bash
docker compose up -d
```

**6. Run**
```bash
uvicorn main:app --reload
```

Open http://localhost:8000 for the UI or http://localhost:8000/docs for the API.

## Testing

```bash
pytest tests/ -v
```
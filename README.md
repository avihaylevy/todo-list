# Todo list

A simple task manager API I built to practice Python backend development.

Built with FastAPI and PostgreSQL running in Docker.

## Stack

- FastAPI + Uvicorn
- PostgreSQL (Docker)
- SQLAlchemy + Alembic
- Pydantic

## Setup

Make sure you have Python 3.11+ and Docker Desktop installed.

**1. Clone and enter the project**
```bash
git clone https://github.com/avihaylevy/todo-list.git
cd todo-api
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
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
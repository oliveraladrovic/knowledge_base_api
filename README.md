# Knowledge Base API

A backend API project built with **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM** and **Alembic**.

This project was created as a practice project for learning how to build a real backend with:
- CRUD operations
- relational database design
- one-to-many and many-to-many relationships
- database migrations
- clean project structure

---

## Features

- **Users**
  - create, read, update and delete users
  - get all notes for a specific user

- **Notes**
  - create, read, update and delete notes
  - get a single note by ID
  - filter notes by tag

- **Tags**
  - create, read, update and delete tags
  - get all tags for a specific note
  - get all notes for a specific tag

- **NoteTag**
  - create, read, update and delete note-tag relationships

- **Other**
  - centralized exception handling
  - API route refactoring with `APIRouter`
  - PostgreSQL database migrations with Alembic

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Poetry

---

## Project Structure

```
src/knowledge_base_api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── services.py
├── exceptions.py
└── routes/
    ├── users.py
    ├── notes.py
    ├── tags.py
    └── note_tags.py
```

---

## Database Relationships

### One-to-Many
- One **User** can have many **Notes**

### Many-to-Many
- One **Note** can have many **Tags**
- One **Tag** can belong to many **Notes**

This is implemented through an association table:

- `note_tags`

---

## API Endpoints

### Health
- `GET /health`

### Users
- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`
- `GET /users/{user_id}/notes`

### Notes
- `POST /notes`
- `GET /notes`
- `GET /notes/{note_id}`
- `PUT /notes/{note_id}`
- `DELETE /notes/{note_id}`

Optional filtering:
- `GET /notes?tag_name=python`

### Tags
- `POST /tags`
- `GET /tags`
- `PUT /tags/{tag_id}`
- `DELETE /tags/{tag_id}`
- `GET /notes/{note_id}/tags`
- `GET /tags/{tag_id}/notes`

### Note Tags
- `POST /note_tags`
- `GET /note_tags`
- `PUT /note_tags/{note_tag_id}`
- `DELETE /note_tags/{note_tag_id}`

---

## Installation

Clone the repository:

```
git clone <your-repo-url>
cd knowledge_base_api
```

Install dependencies:

```
poetry install
```

---

## Environment / Database Setup

Create a PostgreSQL database manually, for example:

```
CREATE DATABASE knowledge_base;
```

Update your database connection in `database.py` and `alembic.ini`.

Example:

```python
DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/knowledge_base"
```

```
sqlalchemy.url = postgresql://postgres:your_password@localhost:5432/knowledge_base
```

---

## Run Migrations

```
poetry run alembic upgrade head
```

---

## Run the API

```
poetry run uvicorn src.knowledge_base_api.main:app --reload
```

---

## Interactive API Docs

Swagger UI is available at:

```
http://127.0.0.1:8000/docs
```

---

## Learning Goals of This Project

This project was built to practice:

- designing relational databases
- working with SQLAlchemy relationships
- using Alembic migrations
- structuring a FastAPI backend project
- separating routes, services and database logic
- handling errors in a centralized way

---

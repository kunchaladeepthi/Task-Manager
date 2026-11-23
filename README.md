# Task Manager

A simple task manager API built with Python and FastAPI.

## Current features

- Create a task with a title.
- View all tasks.
- Return an error for an empty or invalid title.

Tasks are temporarily stored in a Python list. They are cleared when the server restarts.

## Run locally

You need Python installed. Open a terminal in the project folder and run:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs to try the API.

## Current endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/create` | Create a task |
| GET | `/tasks` | View all tasks |

Example request body for creating a task:

```json
{
  "title": "Learn FastAPI"
}
```


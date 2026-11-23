# Task Manager

A simple task manager API built with Python, FastAPI, and SQLite.

## Current features

- Create a task with a title and priority (High, Medium, or Low).
- View all tasks.
- Update a task's title and priority using its ID.
- Delete a task using its ID.
- Return an error for an empty or invalid title.
- Return an error for an invalid priority.

Priority defaults to Medium when omitted from a create or update request. Existing tasks without a priority are assigned Medium automatically.

Tasks are saved in a SQLite database called `tasks.db` in the project folder. The database and tasks table are created automatically when the app starts. Saved tasks remain available after restarting the server.

SQLite support is included with Python, so no separate database installation is needed.

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
| PUT | `/update?id=1` | Update the title and priority of the task with ID 1 |
| DELETE | `/delete?id=1` | Delete the task with ID 1 |

Example request body for creating or updating a task:

```json
{
  "title": "Learn FastAPI",
  "priority": "High"
}
```


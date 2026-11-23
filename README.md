# Task Manager

A simple task manager web app built with FastAPI, SQLite, HTML, CSS, and JavaScript.

## Features

- Add, view, edit, and delete tasks
- Give each task a priority: High, Medium, or Low
- Tasks are saved in a SQLite database, so they are still there after a restart
- Shows 6 tasks per page, with arrow buttons to move between pages
- Works on mobile and desktop

## Project structure

```
app.py             FastAPI app and API endpoints
requirements.txt   Python packages
static/
  index.html       Page layout
  style.css        Styles
  script.js        Calls the API and updates the page
```

The database file `tasks.db` is created automatically the first time the app runs.

## Setup

You need Python 3 installed.

```bash
git clone https://github.com/kunchaladeepthi/Task-Manager.git
cd Task-Manager
python -m venv venv
```

Activate the virtual environment:

- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

Install the packages and start the server:

```bash
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000 to use the app.
Open http://127.0.0.1:8000/docs to try the API.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/tasks?page=1` | Get one page of tasks (6 per page) |
| POST | `/create` | Create a task |
| PUT | `/update?id=1` | Update the task with ID 1 |
| DELETE | `/delete?id=1` | Delete the task with ID 1 |

Request body for creating or updating a task:

```json
{
  "title": "Learn FastAPI",
  "priority": "High"
}
```

The title must be at least 2 characters. Priority is optional and defaults to Medium.

Response from `GET /tasks?page=1`:

```json
{
  "tasks": [{ "id": 1, "title": "Learn FastAPI", "priority": "High" }],
  "page": 1,
  "total_pages": 1,
  "total": 1
}
```

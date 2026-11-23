import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

database_path = Path(__file__).with_name("tasks.db")


def get_connection():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium'
        )
    """)
    columns = connection.execute("PRAGMA table_info(tasks)").fetchall()
    column_names = [column["name"] for column in columns]
    if "priority" not in column_names:
        connection.execute("ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'Medium'")

    connection.commit()
    connection.close()


create_table()

@app.exception_handler(RequestValidationError)
def handle_exception(request, exc):
    message = exc.errors()[0]["msg"]
    return JSONResponse(status_code=422, content={"error": message})


class TaskInput(BaseModel):
    title: str = Field(min_length=2, pattern=r"\S")
    priority: Literal["High", "Medium", "Low"] = "Medium"


@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.post("/create", status_code=201)
def create_task(data: TaskInput):
    title = data.title.strip()
    connection = get_connection()
    cursor = connection.execute(
        "INSERT INTO tasks (title, priority) VALUES (?, ?)",
        (title, data.priority),
    )
    connection.commit()
    task_id = cursor.lastrowid
    connection.close()

    return {"id": task_id, "title": title, "priority": data.priority}


@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    tasks = connection.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    connection.close()
    return [dict(task) for task in tasks]

@app.put("/update")
def update_task(id: int, data: TaskInput):
    title = data.title.strip()
    connection = get_connection()
    cursor = connection.execute(
        "UPDATE tasks SET title = ?, priority = ? WHERE id = ?",
        (title, data.priority, id),
    )
    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated:
        return {"id": id, "title": title, "priority": data.priority}

    return JSONResponse(status_code=404, content={"error": "Task not found"})


@app.delete("/delete")
def delete_task(id: int):
    connection = get_connection()
    task = connection.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()

    if task:
        connection.execute("DELETE FROM tasks WHERE id = ?", (id,))
        connection.commit()

    connection.close()

    if task:
        return {"message": f"Task removed: {task['title']}"}

    return JSONResponse(status_code=404, content={"error": "Task not found"})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)

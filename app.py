from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

tasks = []
next_task_id = 1

@app.exception_handler(RequestValidationError)
def handle_exception(request, exc):
    message = exc.errors()[0]["msg"]
    return JSONResponse(status_code=422, content={"error": message})


class TaskInput(BaseModel):
    title: str = Field(min_length=2, pattern=r"\S")


@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.post("/create", status_code=201)
def create_task(data: TaskInput):
    global next_task_id

    task = {
        "id": next_task_id,
        "title": data.title.strip(),
    }
    tasks.append(task)
    next_task_id += 1

    return task


@app.get("/tasks")
def get_tasks():
    return tasks

@app.put("/update")
def update_task(id: int, data: TaskInput):
    for task in tasks:
        if task["id"] == id:
            task["title"] = data.title.strip()
            return task

    return JSONResponse(status_code=404, content={"error": "Task not found"})


@app.delete("/delete")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return {"message": f"Task removed: {task['title']}"}

    return JSONResponse(status_code=404, content={"error": "Task not found"})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)

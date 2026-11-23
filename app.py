from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

tasks = []

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
    task = {
        "id": len(tasks) + 1,
        "title": data.title.strip(),
    }
    tasks.append(task)

    return task


@app.get("/tasks")
def get_tasks():
    return tasks

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)

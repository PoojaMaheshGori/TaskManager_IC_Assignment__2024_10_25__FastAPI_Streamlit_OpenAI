
'''
pip install fastapi uvicorn
uvicorn src.fastAPI_toDo_app:app --reload
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class ToDoApp:
    def __init__(self):
        self.app = FastAPI()  # Create FastAPI instance
        self.tasks = {}  # In-memory task store

        # Register endpoints with FastAPI
        self.app.add_api_route("/tasks", self.get_all_tasks, methods=["GET"])
        self.app.add_api_route("/tasks/{task_id}", self.get_task, methods=["GET"])
        self.app.add_api_route("/tasks", self.create_task, methods=["POST"])
        self.app.add_api_route("/tasks/{task_id}", self.update_task, methods=["POST"])

    class Task(BaseModel):
        task: str
        description: str

    def get_all_tasks(self):
        """GET: Retrieve all tasks."""
        return self.tasks

    def get_task(self, task_id: int):
        """GET: Retrieve a specific task by ID."""
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        return self.tasks[task_id]

    def create_task(self, task: Task):
        """POST: Create a new task."""
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = task.dict()
        return {"message": "Task created successfully", "task_id": task_id}

    def update_task(self, task_id: int, updated_task: Task):
        """POST: Update an existing task."""
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        self.tasks[task_id] = updated_task.dict()
        return {"message": "Task updated successfully", "task_id": task_id}


# Create an instance of the ToDoApp class
todo_app = ToDoApp()
app = todo_app.app  # Expose the FastAPI app

# Run the application if executed as the main program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastAPI_toDo_app:app", host="127.0.0.1", port=8000, reload=True)

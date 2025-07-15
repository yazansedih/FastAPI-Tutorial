from fastapi import APIRouter, HTTPException
from app.models import Task
from app.fake_db import tasks

router = APIRouter()

@router.get("/tasks")
def get_tasks():
    return tasks

@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}")
def patch_task(task_id: int, patch_data: dict):
    for task in tasks:
        if task.id == task_id:
            for key, value in patch_data.items():
                setattr(task, key, value)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"detail": "Deleted successfully"}

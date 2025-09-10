from fastapi import APIRouter, Response, HTTPException, Depends
from app.schemas import TaskCreate, TaskPatch, TaskOut, GetTasksFilter
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app.models import Task

router = APIRouter(prefix="/tasks", tags=["task"])


@router.post("/", status_code=201)
def add_task(creates: TaskCreate, db: Session = Depends(get_db)):
    task = Task(title=creates.title, done=False)
    task.title_ci = task.title.lower()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="задачи с таким айди нет")
    return task


@router.get("/", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db), params: GetTasksFilter = Depends()):
    query = select(Task)
    if params.done is not None:
        query = query.where(Task.done == params.done)
    if params.q:
        query = query.where(Task.title_ci.contains(params.q.lower()))
    rows = db.execute(query.order_by(Task.id.asc()))
    return rows.scalars().all()


@router.patch("/{task_id}", response_model=TaskOut)
def done_task(task_id: int, payload: TaskPatch, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="задачи с таким айди нет")
    if payload.done is not None:
        task.done = payload.done
    if payload.title is not None:
        t = payload.title.strip()
        if not t:
            raise HTTPException(422, "title пустой")
        task.title = t
        task.title_ci = t.lower()
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="задачи с таким айди нет")
    db.delete(task)
    db.commit()
    return Response(status_code=204)

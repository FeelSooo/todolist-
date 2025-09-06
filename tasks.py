from fastapi import APIRouter, Request, HTTPException, Depends
from schemas import TaskCreate, TaskPatch, GetTasksFilter


router = APIRouter(prefix="/tasks", tags=["task"])


@router.post("/", status_code=201)
def add_task(request: Request, creates: TaskCreate):
    tasks = request.app.state.tasks
    tid = next(request.app.state.id_seq)
    tasks[tid] = {"title": creates.title, "done": False}
    return {"id": tid, **tasks[tid]}


@router.get("/{task_id}")
def get_task(task_id: int, request: Request):
    tasks = request.app.state.tasks
    item = tasks.get(task_id)
    if item is None:
        raise HTTPException(status_code=404, detail="задачи с таким айди нет")
    else:
        return item
    

@router.get("/")
def get_tasks(request: Request, params:GetTasksFilter = Depends()):
    tasks = request.app.state.tasks
    items = [{"id": i, **obj} for i,obj in tasks.items()]

    if params.done is not None:
        items = [t for t in items if t["done"] == params.done]
    if params.q:
        s = params.q.lower()
        items = [t for t in items if s in t["title"].lower()]

    return items

@router.patch("/{task_id}")
def done_task(task_id: int, request: Request, payload: TaskPatch):
    tasks = request.app.state.tasks
    item = tasks.get(task_id)
    if item is None:
        raise HTTPException(status_code=404, detail="задачи с таким айди нет")
    if payload.done is not None:
        item["done"] = payload.done
        return item


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, request: Request):
    tasks = request.app.state.tasks
    if task_id not in tasks:
        raise HTTPException(status_code=404,detail="задачи с таким айди нет")
    del tasks[task_id]
    return {"msg": "task removed"}
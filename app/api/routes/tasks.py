from fastapi import APIRouter, Response, HTTPException, Depends

from app.api.filters.tasks import GetTasksFilter
from app.api.requests.tasks import CreateTaskRequest, UpdateTaskRequest
from app.api.responses.tasks import TaskResponse, TasksRequest

from app.models.task import Task

from app.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["task"])


# @router.post("/", response_model=TaskResponse,_status_code=201)
# async def add_task(payload: CreateTaskRequest, service:TasksService = Depends(TasksService)):
#     # task = await service.create_task(payload) 
#     # return task
#     pass


# @router.get("/{task_id}", response_model=TaskOut)
# def get_task(task_id: int, db: Session = Depends(get_session)):
#     task = db.get(Task, task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="задачи с таким айди нет")
#     return task


@router.get("/", response_model=TasksRequest)
async def get_tasks(
    filters: GetTasksFilter = Depends(), service: TasksService = Depends(TasksService)
):
    return await service.get_tasks(filters=filters)


# @router.patch("/{task_id}", response_model=TaskOut)
# def done_task(task_id: int, payload: TaskPatch, db: Session = Depends(get_session)):
#     task = db.get(Task, task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="задачи с таким айди нет")
#     if payload.done is not None:
#         task.done = payload.done
#     if payload.title is not None:
#         t = payload.title.strip()
#         if not t:
#             raise HTTPException(422, "title пустой")
#         task.title = t
#         task.title_ci = t.lower()
#     db.commit()
#     db.refresh(task)
#     return task


# @router.delete("/{task_id}", status_code=204)
# def delete_task(task_id: int, db: Session = Depends(get_session)):
#     task = db.get(Task, task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="задачи с таким айди нет")
#     db.delete(task)
#     db.commit()
#     return Response(status_code=204)

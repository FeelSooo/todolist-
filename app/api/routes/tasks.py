from fastapi import APIRouter, Response, HTTPException, Depends
from app.schemas import TaskCreate, TaskPatch, TaskOut, GetTasksFilter
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.task import Task
from app.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["task"])


# @router.post("/", status_code=201)
# def add_task(creates: TaskCreate, db: Session = Depends(get_db)):
#     task = Task(title=creates.title, done=False)
#     task.title_ci = task.title.lower()
#     db.add(task)
#     db.commit()
#     db.refresh(task)
#     return task
#
#
# @router.get("/{task_id}", response_model=TaskOut)
# def get_task(
#     task_id: int,
#     db: Session = Depends(get_db),
# ):
#     task = db.get(Task, task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="задачи с таким айди нет")
#     return task
#


@router.get(
    "/",
    response_model=list[TaskOut],
)
async def get_tasks(
    filters: GetTasksFilter = Depends(),
    service: TasksService = Depends(TasksService),
):
    return await service.get_tasks(
        filters=filters,
    )


# @router.patch(
#     "/{task_id}",
#     response_model=TaskOut,
# )
# def done_task(task_id: int, payload: TaskPatch, db: Session = Depends(get_db)):
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
#
#
# @router.delete(
#     "/{task_id}",
#     status_code=204,
# )
# def delete_task(task_id: int, db: Session = Depends(get_db)):
#     task = db.get(Task, task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="задачи с таким айди нет")
#     db.delete(task)
#     db.commit()
#     return Response(status_code=204)

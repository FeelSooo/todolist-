from fastapi import APIRouter, status, Depends

from app.api.filters.tasks import GetTasksFilter
from app.api.requests.tasks import TaskCreate, TaskUpdate
from app.api.responses.tasks import TaskResponse, TaskEnvelope, TasksEnvelope

from app.services.tasks import TasksService

router = APIRouter(prefix="/tasks", tags=["task"])


@router.post("/", response_model=TaskEnvelope,status_code=status.HTTP_201_CREATED)
async def add_task(payload: TaskCreate, service:TasksService = Depends(TasksService.provider)):
    task = await service.create_tasks(payload) 
    return {"result": task}    


@router.get("/{task_id}", response_model=TaskEnvelope)
async def get_task(task_id: int, service:TasksService = Depends(TasksService.provider)):
    task: TaskResponse = await service.get_task(task_id)
    return {"result": task}


@router.get("/", response_model=TasksEnvelope)
async def get_tasks(
    filters: GetTasksFilter = Depends(), service: TasksService = Depends(TasksService.provider)
):
    tasks: list[TaskResponse] = await service.get_tasks(filters=filters)
    return {"result": tasks}


@router.patch("/{task_id}", response_model=TaskEnvelope, status_code=status.HTTP_200_OK)
async def patch_task(task_id: int, payload:TaskUpdate = ..., service: TasksService = Depends(TasksService.provider)):
    task: TaskResponse = await service.patch_task(task_id, payload)
    return {"result": task}


# @router.delete("/{task_id}", status_code=204)
# def delete_task(task_id: int, db: Session = Depends(get_session)):
#     task = db.get(Task, task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="задачи с таким айди нет")
#     db.delete(task)
#     db.commit()
#     return Response(status_code=204)

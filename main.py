from fastapi import FastAPI
from tasks import router as task_router
from itertools import count


app = FastAPI()

# общий стейт
app.state.tasks = {}
app.state.id_seq = count()    


#включаю эндпоинты
app.include_router(task_router)
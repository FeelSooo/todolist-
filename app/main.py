from fastapi import FastAPI
from app.tasks import router as task_router
from app.db import engine
from app.models import Base


app = FastAPI()

Base.metadata.create_all(bind=engine)

# общий стейт
# app.state.tasks = {}
# app.state.id_seq = count()    


#включаю эндпоинты
app.include_router(task_router)
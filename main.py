from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import init_db
from requests import get_tasks, get_completed_tasks_count


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print('Server is ready')
    yield


app = FastAPI(title="Web App", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks/{user_id}")
async def tasks(user_id: int):
    return await get_tasks(user_id)


@app.get("/api/main/{user_id}")
async def profile(user_id: int):
    completed_tasks_count = await get_completed_tasks_count(user_id)
    return {'completedTasks': completed_tasks_count}
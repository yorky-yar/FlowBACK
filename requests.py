from sqlalchemy import select, func
from models import async_session, User, Task
from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    id: int
    title: str
    completed: bool
    user: int

    model_config = ConfigDict(from_attributes=True)


async def add_user(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        if user:
            return user
        
        new_user = User(user_id=user_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_tasks(user_id):
    async with async_session() as session:
        user = await add_user(user_id)
        tasks = await session.scalars(
            select(Task).where(Task.user == user.id, Task.completed == False)
        )

        serialized_tasks = [
            TaskSchema.model_validate(t).model_dump() for t in tasks
        ]

        return serialized_tasks


async def get_completed_tasks_count(user_id):
    async with async_session() as session:
        user = await add_user(user_id)
        return await session.scalar(
            select(func.count(Task.id))
            .where(Task.completed == True, Task.user == user.id)
        )
import asyncio
from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession 
from .models import (
    Session,
    async_engine, 
    Base, 
    User, 
    Post, 
    )

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
async def create_user(
    session: AsyncSession,
    username: str,
    email: str | None = None,
) -> User:
    user = User(username=username, email=email)
    session.add(user)
    await session.commit()
    return user


async def create_post(
    session: AsyncSession,
    title: str,
    user_id: int,
    body: str,
) -> Post:
    post = Post(title=title, user_id=user_id, body=body)
    session.add(post)
    await session.commit()
    return post


async def fetch_all_posts_with_authors(
    session: AsyncSession,
) -> Sequence[Post]:
    stmt = (
        select(Post)
        .options(
            selectinload(Post.user),
            selectinload(Post.body)
        )
        .order_by(Post.id)
    )
    result = await session.execute(stmt)
    return result


async def async_main():
    await create_tables()
    async with Session() as session:
        task_1 = await create_user(session, username = "Sam", email="Sam@mail.ru")
        task_1=await asyncio.gather(task_1)
        
        

       

if __name__ == "__main__":
    asyncio.run(async_main())
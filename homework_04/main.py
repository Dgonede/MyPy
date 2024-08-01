import asyncio
from collections.abc import Sequence
from sqlalchemy import desc, select
import aiohttp
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from jsonplaceholder_requests import USERS_DATA_URL, POSTS_DATA_URL
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


async def fetch_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


async def fetch_all_posts(session: AsyncSession):
    result = await session.execute(select(Post))
    return result.scalars().all()

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def fetch_users_data():
    return await fetch_json(USERS_DATA_URL)

async def fetch_posts_data():
    return await fetch_json(POSTS_DATA_URL)
   
async def async_main():
    users_data = await fetch_users_data()
    posts_data = await fetch_posts_data()
    await create_tables()
    async with Session() as session:
        users_data = await fetch_users_data()
        posts_data = await fetch_posts_data()
        
        # Создание пользователей и постов в базе данных
        for user_data in users_data:
            await create_user(session, username=user_data['username'], email=user_data['email'])
        
        for post_data in posts_data:
            user_id = post_data['userId']  # Предполагаем, что userId соответствует id в базе данных
            await create_post(session, title=post_data['title'], body=post_data['body'], user_id=user_id)
        
        # Получение всех пользователей и постов
        users = await fetch_all_users(session)
        posts = await fetch_all_posts(session)
        return users, posts
       
        
       

if __name__ == "__main__":
    asyncio.run(async_main())
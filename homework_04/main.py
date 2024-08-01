import asyncio
from collections.abc import Sequence
from sqlalchemy import desc, select
import logging
import aiohttp
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .models import (
    Session,
    async_engine, 
    Base, 
    User, 
    Post, 
    )

# Настройка логирования
log = logging.getLogger(__name__)


# Определение URL для получения данных
USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"



# Асинхронные функции для работы с базой данных
async def create_user(session: AsyncSession, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def create_post(session: AsyncSession, title: str, body: str, user_id: int) -> Post:
    post = Post(title=title, body=body, user_id=user_id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def fetch_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

async def fetch_all_posts(session: AsyncSession):
    result = await session.execute(select(Post))
    return result.scalars().all()

# Функция для получения данных из API
async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def fetch_users_data():
    return await fetch_json(USERS_DATA_URL)

async def fetch_posts_data():
    return await fetch_json(POSTS_DATA_URL)

async def main():
    logging.basicConfig(level=logging.INFO)
    log.warning("Starting main")
    
    async with Session() as session:
        # Получение данных пользователей и постов
        users_data = await fetch_users_data()
        posts_data = await fetch_posts_data()
        
        # Создание пользователей в базе данных
        user_map = {}  # Словарь для сопоставления username и id
        for user_data in users_data:
            user = await create_user(session, username=user_data['username'], email=user_data['email'])
            user_map[user_data['id']] = user.id  # Сохраняем соответствие userId и id в базе данных
        
        # Создание постов в базе данных
        for post_data in posts_data:
            user_id = user_map.get(post_data['userId'])  # Получаем id пользователя из user_map
            if user_id:  # Проверяем, существует ли пользователь
                await create_post(session, title=post_data['title'], body=post_data['body'], user_id=user_id)
        
        # Получение всех пользователей и постов
        users = await fetch_all_users(session)
        posts = await fetch_all_posts(session)
        
        log.info("Fetched users: %s", users)
        log.info("Fetched posts: %s", posts)
    
    log.warning("Finished main")

if __name__ == "__main__":
    asyncio.run(main())
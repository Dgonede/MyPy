import asyncio
from collections.abc import Sequence
import os
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    Session,
    async_engine, 
    Base, 
    User, 
    Post, 
    )

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # # Base.metadata.drop_all(bind=engine)
    # print("Creating tables...", Base.metadata.tables)
    # Base.metadata.create_all(bind=engine)

async def create_user(
    session: AsyncSession,
    username: str,
    email: str | None = None,
) -> User:
    user = User(username=username, email=email)
    session.add(user)

    await session.commit()

    print("user created:", user)
    return user


async def create_post(
    session: AsyncSession,
    title: str,
    user_id: int,
) -> Post:
    post = Post(title=title, user_id=user_id)
    # post.author = user
    session.add(post)
    await session.commit()
    print("post created:", post)
    return post


async def fetch_all_posts_with_authors(
    session: AsyncSession,
) -> Sequence[Post]:
    stmt = (
        select(Post)
        .options(
            joinedload(Post.author),
        )
        .order_by(Post.id)
    )
    result = await session.scalars(stmt)
    posts = result.all()
    print("posts:", posts)

    for post in posts:
        print("+", post)
        print("= author:", post.author)

    return posts


async def main():
    await create_tables()
    async with Session() as session:
        await create_user(session, username="lone", email="lone@admin.com")
        gane: User = await create_user(session, username="gane", email=None)
        post_pg: Post = await create_post(
            session=session,
            title="Reander post",
            user_id=gane.id,
           
        )
        print("post pg:", post_pg)

    await fetch_all_posts_with_authors(session) 
       

   


      
        

if __name__ == "__main__":
    asyncio.run(main())
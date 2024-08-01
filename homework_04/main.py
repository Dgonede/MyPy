import asyncio
from collections.abc import Sequence
from sqlalchemy import desc, select
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


async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(desc(User.username))
    result = await session.scalars(stmt)
    users = result.all()
    return users


async def fetch_all_posts(session: AsyncSession) -> Sequence[Post]:
    stmt = select(Post).order_by(Post.id)
    result = await session.scalars(stmt)
    posts = result.all()
    return posts



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
        await asyncio.gather(create_user(session, username="admin", email="admin@admin.com"))
        bob: User = await create_user(session, username="bob", email=None)
        john: User = await create_user(session, username="john", email=None)
        greg: User = await create_user(session, username="greg", email=None)
        post_pg: Post = await asyncio.gather(create_post(
            session=session,
            title="PostgreSQL news",
            user_id=greg.id,
            body="PUSTO",
        ))

        
    await asyncio.gather(fetch_all_users(session))  
    await asyncio.gather(fetch_all_posts(session))  
    
        
        
        
def main():
    async_main()        
      
       

if __name__ == "__main__":
    asyncio.run(main())
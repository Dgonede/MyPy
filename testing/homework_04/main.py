import asyncio
from collections.abc import Sequence

from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from models.models import (
    async_session,
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


async def create_users(
    session: AsyncSession,
    *usernames: str,
) -> Sequence[User]:
    users = [
        User(username=username)
        for username in usernames
    ]
    session.add_all(users)
    print("prepared users:", users)

    await session.commit()

    print("saved users:", users)
    return users


async def create_posts(
    session: AsyncSession,
    *titles: str,
    user_id: int,
) -> Sequence[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in titles
    ]
    session.add_all(posts)
    print("prepared posts:", posts)
    await session.commit()
    print("saved posts:", posts)
    return posts





async def create_tags(
    session: AsyncSession,
    *names: str,
) -> Sequence[Tag]:
    tags = [
        Tag(name=name)
        for name in names
    ]
    session.add_all(tags)
    print("prepared tags:", tags)
    await session.commit()
    print("saved tags:", tags)
    return tags

async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    # stmt = select(User).order_by(User.id)
    stmt = select(User).order_by(desc(User.username))
    # result = session.execute(stmt)
    # users = result.scalars().all()
    result = await session.scalars(stmt)
    users = result.all()
    print("users:", users)
    return users


async def fetch_users_with_posts(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )

    print("load users w/ posts:")
    # users = session.scalars(stmt).unique().all()
    result = await session.scalars(stmt)
    users = result.all()
    for user in users:
        print("+", user)
        for post in user.posts:
            print("  -", post)

    return users


async def fetch_all_posts(session: AsyncSession) -> Sequence[Post]:
    stmt = select(Post).order_by(Post.id)
    # result = session.execute(stmt)
    # posts = result.scalars().all()
    result = await session.scalars(stmt)
    posts = result.all()
    print("posts:", posts)
    return posts


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


async def fetch_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result = session.execute(stmt)
    # user = result.scalars().one_or_none()
    user: User | None = session.scalars(stmt).one_or_none()
    print("user for username", repr(username), "result:", user)
    return user


SQL = """
UPDATE users 
SET email=concat(
    lower(users.username), 
    '@ya.ru'::VARCHAR
)
WHERE users.email IS NULL 
    AND length(users.username) < 5::INTEGER;
"""


async def set_emails_for_null_email_users_with_username_limit(
    session: AsyncSession,
    username_size_limit: int,
    domain: str,
):
    """

    :param session:
    :param username_size_limit:
    :param domain: example: '@ya.ru'
    :return:
    """

    new_email = (
        func.concat(
            func.lower(User.username),
            domain.lower(),
        )
    )
    stmt = (
        update(User)
        .where(
            # empty email
            User.email.is_(None),
            # username len limit
            func.length(User.username) < username_size_limit,
        )
        .values(
            {
                User.email: new_email,
            }
        )
    )

    await session.execute(stmt)
    await session.commit()



async def set_body_for_null_post_table(
    session: AsyncSession,
    title_size_limit: int,
    
):
    """

    :param session:
    :param username_size_limit:
    :param domain: example: '@ya.ru'
    :return:
    """

    new_body = (
        func.concat(
            func.upper(Post.title),
            Post.body == Post.title,
        )
    )
    stmt = (
        update(Post)
        .where(
            
            Post.body.is_(None),
            
            func.length(Post.title) < title_size_limit,
        )
        .values(
            {
                Post.body: new_body,
            }
        )
    )

    await session.execute(stmt)
    await session.commit()


async def select_top_users_with_posts_sorted(
    session: AsyncSession,
) -> None:
    users_w_posts_count_stmt = (
        select(User, func.count(Post.id).label('posts_count'))
        .join(User.posts, isouter=True)
        .group_by(User.id)
        .order_by(func.count(Post.id).desc(), User.username)
    )
    result = await session.execute(users_w_posts_count_stmt)
    result = result.all()
    for user, posts_count in result:
        print("+ user", user.id, user.username, "w/", posts_count, "posts")


async def main():
    await create_tables()
    # async with async_session() as session:
    #     await create_user(session, username="lone", email="lone@admin.com")
    #     gane: User = await create_user(session, username="gane", email=None)
    #     post_pg: Post = await create_post(
    #         session=session,
    #         title="Reander post",
    #         user_id=gane.id,
           
    #     )
    #     print("post pg:", post_pg)
    #     await create_users(session, "nick", "bob", "alice")
    #     sam: User = await create_user(session, username="sam", email=None)
    #     await create_posts(
    #         session,
    #         "MySQL Intro",
    #         "MariaDB Lesson",
    #         user_id=sam.id,
            
    #     )

    #     # await create_tags(session, "news", "postgres", "MySql")


    #     await fetch_all_users(session)
    #     await fetch_users_with_posts(session)

    #     await fetch_all_posts(session)
        # posts: Sequence[Post] = await fetch_all_posts_with_authors(session)
        #
        # for post in posts:
        #     print("+", post)
        #     print("= author:", post.author)

        # await fetch_user_by_username(session, "bob")
        # await fetch_user_by_username(session, "jack")
        # await set_emails_for_null_email_users_with_username_limit(
        # #     session,
        # #     username_size_limit=5,
        # #     domain="@ya.ru",
        # # )
        # await set_body_for_null_post_table(session, title_size_limit=20)



        # await select_top_users_with_posts_sorted(session)

        # запрашиваем посты авторов, у кого юзернейм длиной более 3 символов
        # stmt = (
        #     select(Post)
        #     # .join(User)
        #     # .join(User, Post.user_id == User.id)
        #     .join(Post.author)
        #     .where(func.length(User.username) > 3)
        #     .options(
        #         # joinedload(Post.author),
        #         selectinload(Post.author),
        #     )
        #     .order_by(Post.id)
        # )
        #
        # posts = session.scalars(stmt).all()
        # print(posts)


if __name__ == "__main__":
    asyncio.run(main())
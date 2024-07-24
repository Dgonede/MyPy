import aiohttp
import asyncio
import logging

log = logging.getLogger(__name__)

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"

def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    )


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
    configure_logging()
    log.warning("Starting main")
    async with asyncio. TaskGroup() as tg:
        task1 = tg.create_task(fetch_users_data())
        task2 = tg.create_task(fetch_posts_data())
    log.info("Fetched data (1): %s", task1.result())
    print()
    print()
    print()
    log.info("Fetched data (2): %s", task2.result())
    log.warning("Finished main")


if __name__=="__main__":
    asyncio.run(main())
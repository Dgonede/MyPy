import asyncio
import asyncpg

async def connect_to_db():
    dsn = "postgresql://postgres:password@localhost/postgres"
    conn = await asyncpg.connect(dsn)
    
    # Выполнение запросов к базе данных
    result = await conn.fetch("SELECT * FROM your_table")
    print(result)
    
    await conn.close()

# Запуск асинхронной функции подключения к базе данных
asyncio.get_event_loop().run_until_complete(connect_to_db())
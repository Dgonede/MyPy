from os import getenv


DB_URL = "postgresql+psycopg://user:password@localhost:5432/blog"
DB_ECHO = getenv("DB_ECHO", False)
if DB_ECHO =="0":
    DB_ECHO = False
# from sqlalchemy import MetaData
# from sqlalchemy import Table
# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import String
# from db import engine


# metadata = MetaData()

# authors_table = Table(
#     name="authors",
#     metadata,
#     Column(name="id", Integer, primary_key=True),
#     Column(name="username", String, nullable=False, unique=True),
#     Column(name="email", String, nullable=True, unique=True),
# )

# def create_table():
#     metadata.create_all(bind=engine)
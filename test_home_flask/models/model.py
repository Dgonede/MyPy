from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer

db = SQLAlchemy()


class Owner(db.Model):
    id: Mapped[int] = mapped_column(Integer(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    order: Mapped[list["Orders"]] = relationship(back_populates="Owner")


class Orders(db.Model):
    id: Mapped[int] = mapped_column(Integer(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    breed: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    owner: Mapped["Owner"] = relationship(back_populates="order")

     

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base



# if TYPE_CHECKING:
#     from .user import User


class Tag(Base):

    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name!r}"
            ")"
        )
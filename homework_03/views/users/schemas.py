import uuid
from pydantic import BaseModel, EmailStr, Field


UserIdType = int

class UserBase(BaseModel):
    Admin: str | None
    username: str
    email: EmailStr
    password: str | None 
    


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: UserIdType = Field(
        ...,
        description="The id of the user",
        example=42,
    )


def generate_user_token() -> str:
    token = str(uuid.uuid4())
    print("New token:", token)
    return token

class User(UserBase):
    id: UserIdType
    token: str = Field(default_factory=generate_user_token)
    password: str | None

class UserAdmin(UserBase):
    id: UserIdType
    token: str = Field(default_factory=generate_user_token)
    password: str | None
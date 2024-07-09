from pydantic import BaseModel
from .schemas import User, UserCreate, UserIdType

class UsersStorage(BaseModel):
    users: dict[UserIdType, User] = {}
    users_by_token: dict[str, User] = {}
    user_by_password: dict[str, User] = {}
    last_id: int = 0

    @property
    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id
    
    def create(self, user_in: UserCreate) -> User:
        user = User(
            id = self.next_id,
            **user_in.model_dump(),
        )
        self.users[user.id] = user
        self.users_by_token[user.token] = user
        self.user_by_password[user.password] = user
        return user 
    
    def get(self) -> list[User]:
        return list(self.users.values())
    
    def get_by_id(self, user_id: UserIdType) -> User | None:
        return self.users.get(user_id)
    
    def get_by_token(self,token: str) -> User | None:
        return self.users_by_token.get(token)
    
    def get_by_pass(self, password: str) -> User | None:
        return self.user_by_password.get(password)
    
storage = UsersStorage()
Admin = "Admin"
storage.create(
    UserCreate(
        Admin= "Admin",
        username= "Admin",
        email="admin@ya.ru",
        password= "ADMIN123123"
    ),
)


storage.create(
    UserCreate(
        Admin = None,
        username= "sam",
        email="sam@ya.ru",
        password="SAMSAMSAM"
    ),
)


storage.create(
    UserCreate(
        Admin = None,
        username= "bob",
        email="bob@ya.ru",
        password= None
    ),
)


storage.create(
    UserCreate(
        Admin = "Admin2",
        username= "jhon",
        email="jhon@ya.ru",
        password = "O23@#OE"
    ),
)
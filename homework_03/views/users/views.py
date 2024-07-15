from fastapi import APIRouter, Depends, HTTPException, status
from views.users.depenencies import get_user_by_pass
from views.users.schemas import User, UserCreate, UserRead
from .crud import storage
from pydantic import PositiveInt


router = APIRouter(
    prefix="/users",
    tags=["Верхний уровень/для доступа требуется авторизация"],
)




password_entared = False   


"""Основная авторизация для дальнешей работы с Api"""  
@router.get("/me/", response_model=UserRead)
def get_me(
     user:User = Depends(get_user_by_pass),
     ):
     global password_entared
     if user.Admin:
          password_entared = True,
          return user
          
     raise HTTPException(
          status_code=status.HTTP_423_LOCKED,
          detail="Ooops, only for Administrator's ;)"
    )




"""Получаем список пользователей если пройдена авторизация"""
@router.get(
        "/",
        response_model=list[UserRead],
)

def get_users_list():
     if not password_entared:
          raise HTTPException(
               status_code=status.HTTP_423_LOCKED,
               detail="Please authenticate first"
               )
     else:
          return storage.get()




"""Добавляем нового пользователя если пройдена авторизация"""
@router.post(
          "/",
          status_code= status.HTTP_201_CREATED, 
          response_model = UserRead,
          )

def create_user(
     user_in: UserCreate,
):
     if  not password_entared:
          raise HTTPException(
               status_code=status.HTTP_423_LOCKED,
               detail="Please authenticate first"
               )
     else:
          return storage.create(user_in=user_in)




"""Достаем пользователя по id если пройдена авторизация"""
@router.get(
    "/{user_id}/", 
    response_model = UserRead,
    responses={
        status.HTTP_404_NOT_FOUND:{
            "discription": "User not found",
            "content": {
                 "application/json": {
                     "example": {
                        "detail": "User #{user_id} not found"
                    },
                },
            },
        },
    },
)

def  get_user(user_id: PositiveInt):
     user = storage.get_by_id(user_id=user_id)
     if not password_entared:
          raise HTTPException(
               status_code=status.HTTP_423_LOCKED,
               detail="Please authenticate first"
               )
     if user:
          return user
     raise HTTPException(
          status_code = status.HTTP_404_NOT_FOUND,
          detail = f"User #{user_id} not found",
     )



     
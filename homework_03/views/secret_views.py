
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field


router = APIRouter(
    tags=["secret"]
)

"""Класс с примером успешного ввода токена"""
class SecretInfo(BaseModel):
    answer: int = Field(example = 33)
    token: str = Field(
        example = "tutor-of-api", 
        description = "The secret token provided by user")

"""Обозначаем валидные токены для входа"""
VALID_TOKENS = {
    "rette",
    "qwette",
    "foobar",
}

"""Создаем функицию проверяющую валидность данных токена"""
def check_token(token: str = Header(alias="x-secret-token")) -> str:
    if token in VALID_TOKENS:
        return token
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )

"""Создаем пример в случаи ошибки ввода данных и возвращаем ответ при валидном токене"""
@router.get(
    "/secret/",
    response_model= SecretInfo,
    responses={
        status.HTTP_404_NOT_FOUND:{
            "discription": "invalid token provided",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid token"
                    },
                },
            },
        },
    },
)
def get_secret(
    token: Annotated[str, Depends(check_token)],
):
    return {
        "answer": 42,
        "token": token,
    }
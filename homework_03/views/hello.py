from typing import Annotated
from annotated_types import MaxLen, MinLen
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/hello/", tags = ["Нижный уровень/авторизация не требуется"])
def  hello_name(
    name: Annotated[str, MinLen(3), MaxLen(10)],
    ):
    return {"message": f"Hello, {name}!"}



@router.get("/hello-html/", response_class=HTMLResponse, tags = ["Нижный уровень/авторизация не требуется"])
def hello_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello Page</title>
</head>
<body>
    <h1>Hellow Page</h1>
</body>
</html>
"""

from typing import Annotated

from annotated_types import Ge, Lt
from fastapi import APIRouter

router = APIRouter(
    prefix = "/items",
    tags = ["items"],
)
    
@router.get("/")
def get_items():
    return {
        "data": [
            {"id": 1, "name": "qwerty"},
            {"id": 2, "name": "foobar"},
        ],
    }    


@router.get("/{item_id}/")
def get_item(
    item_id: Annotated[int, Ge(1), Lt(10_000)],
             ):
    return {
        "data": {"id": item_id, "name": "abc"}
    }

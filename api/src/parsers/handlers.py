from .parser_promptbase import get_categories as categ
from .parser_promptbase import get_promt_by_category
from enums import CategoryEnum

from fastapi import APIRouter

import time


router = APIRouter()


@router.get("/categories")
async def get_categories():
    """Получает категории"""
    categories = await categ()

    return {"Категории": categories}


@router.post("/promts")
async def get_promts(category_name: CategoryEnum, count: int):
    """Выдаёт промты по выбранной категории"""
    promts = await get_promt_by_category(category=category_name.value, count=count)

    return {"Промты": promts}

from http import HTTPStatus

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.dto.categories import (
    CreateCategoryDto,
    ReadCategoriesDto,
    ReadCategoryDto,
    UpdateCategoryDto,
)
from app.services.categories import CategoriesService

router = APIRouter(prefix='/categories', tags=['Categories 🗂️'])


@router.get('/')
@inject
async def get_categories(service: FromDishka[CategoriesService]) -> ReadCategoriesDto:
    return await service.get_all_categories()


@router.get('/{category_id}')
@inject
async def get_category(service: FromDishka[CategoriesService], category_id: int) -> ReadCategoryDto:
    return await service.get_category_by_id(category_id)


@router.post('/', status_code=HTTPStatus.CREATED)
@inject
async def create_category(
    service: FromDishka[CategoriesService],
    payload: CreateCategoryDto,
) -> ReadCategoryDto:
    return await service.create_category(payload)


@router.put('/{category_id}')
@inject
async def update_category(
    service: FromDishka[CategoriesService],
    payload: UpdateCategoryDto,
    category_id: int,
) -> ReadCategoryDto:
    return await service.update_category(category_id, payload)


@router.delete('/{category_id}', status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete_category(
    service: FromDishka[CategoriesService],
    category_id: int,
) -> None:
    return await service.delete_category(category_id)

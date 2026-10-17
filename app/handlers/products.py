from http import HTTPStatus

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from app.dto.products import (
    CreateProductDto,
    ReadProductDto,
    ReadProductsDto,
    UpdateProductDto,
)
from app.services.products import ProductsService

router = APIRouter(prefix='/products', tags=['Products 📦'])


@router.get('/')
@inject
async def get_products(product_service: FromDishka[ProductsService]) -> ReadProductsDto:
    return await product_service.get_products()


@router.get('/{product_id}')
@inject
async def get_product_by_id(product_service: FromDishka[ProductsService], product_id: int) -> ReadProductDto:
    return await product_service.get_product_by_id(product_id)


@router.get('/categories/{category_id}')
@inject
async def get_products_by_category_id(
    product_service: FromDishka[ProductsService], category_id: int
) -> ReadProductsDto:
    return await product_service.get_products_by_category(category_id)


@router.post('/', status_code=HTTPStatus.CREATED)
@inject
async def create_products(product_service: FromDishka[ProductsService], payload: CreateProductDto) -> ReadProductDto:
    return await product_service.create_product(payload)


@router.put('/{product_id}')
@inject
async def update_products(
    product_service: FromDishka[ProductsService],
    payload: UpdateProductDto,
    product_id: int,
) -> ReadProductDto:
    return await product_service.update_product(product_id, payload)


@router.delete('/{product_id}', status_code=HTTPStatus.NO_CONTENT)
@inject
async def delete_products(product_service: FromDishka[ProductsService], product_id: int) -> None:
    return await product_service.delete_product(product_id)

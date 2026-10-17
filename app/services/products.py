from dishka import Scope
from orderflow_core.di import injectable

from app.dao.products import ProductsDao
from app.dto.products import (
    CreateProductDto,
    ReadProductDto,
    ReadProductsDto,
    UpdateProductDto,
)
from app.exceptions.products import ProductAlreadyExistsError, ProductNotFoundError
from app.services.categories import CategoriesService


@injectable(scope=Scope.REQUEST)
class ProductsService:
    def __init__(self, product_dao: ProductsDao, category_service: CategoriesService):
        self.product_dao = product_dao
        self.category_service = category_service

    async def get_products(self) -> ReadProductsDto:
        return ReadProductsDto.model_validate(await self.product_dao.get_products())

    async def get_product_by_id(self, product_id: int) -> ReadProductDto:
        await self._check_product_exists(product_id)
        return ReadProductDto.model_validate(await self.product_dao.get_product_by_id(product_id))

    async def get_products_by_category(self, category_id: int) -> ReadProductsDto:
        await self.category_service.check_category_exists(category_id)
        return ReadProductsDto.model_validate(await self.product_dao.get_products_by_category(category_id))

    async def create_product(self, payload: CreateProductDto) -> ReadProductDto:
        await self.category_service.check_category_exists(payload.category_id)
        await self._check_product_name_already_exists(payload.name)
        return ReadProductDto.model_validate(await self.product_dao.create_product(payload))

    async def update_product(self, product_id: int, payload: UpdateProductDto) -> ReadProductDto:
        await self.category_service.check_category_exists(payload.category_id)
        await self._check_product_name_already_exists(payload.name, product_id)
        return ReadProductDto.model_validate(await self.product_dao.update_product(product_id, payload))

    async def delete_product(self, product_id: int) -> None:
        await self._check_product_exists(product_id)
        await self.product_dao.delete_product(product_id)

    async def _check_product_exists(self, product_id: int) -> None:
        if not await self.product_dao.get_product_by_id(product_id):
            raise ProductNotFoundError(product_id)

    async def _check_product_name_already_exists(
        self, product_name: str, exclude_product_id: int | None = None
    ) -> None:
        if await self.product_dao.get_product_by_name(product_name, exclude_product_id):
            raise ProductAlreadyExistsError(product_name)

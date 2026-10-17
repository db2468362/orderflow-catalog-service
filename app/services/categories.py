from dishka import Scope
from orderflow_core.di import injectable

from app.dao.categories import CategoriesDao
from app.dto.categories import (
    CreateCategoryDto,
    ReadCategoriesDto,
    ReadCategoryDto,
    UpdateCategoryDto,
)
from app.exceptions.categories import CategoryAlreadyExistsError, CategoryNotFoundError


@injectable(scope=Scope.REQUEST)
class CategoriesService:
    def __init__(self, dao: CategoriesDao) -> None:
        self.dao = dao

    async def get_all_categories(self) -> ReadCategoriesDto:
        result = await self.dao.get_categories()
        return ReadCategoriesDto.model_validate(result)

    async def get_category_by_id(self, category_id: int) -> ReadCategoryDto:
        await self.check_category_exists(category_id)
        result = await self.dao.get_category_by_id(category_id)
        return ReadCategoryDto.model_validate(result)

    async def create_category(self, payload: CreateCategoryDto) -> ReadCategoryDto:
        await self._check_category_name_already_exists(payload.name)
        result = await self.dao.create_category(payload)
        return ReadCategoryDto.model_validate(result)

    async def update_category(self, category_id: int, payload: UpdateCategoryDto) -> ReadCategoryDto:
        await self.check_category_exists(category_id)
        await self._check_category_name_already_exists(payload.name, category_id)
        result = await self.dao.update_category(category_id, payload)
        return ReadCategoryDto.model_validate(result)

    async def delete_category(self, category_id: int) -> None:
        await self.check_category_exists(category_id)
        await self.dao.delete_category(category_id)

    async def check_category_exists(self, category_id: int) -> None:
        if not await self.dao.get_category_by_id(category_id):
            raise CategoryNotFoundError(category_id)

    async def _check_category_name_already_exists(
        self, category_name: str, exclude_category_id: int | None = None
    ) -> None:
        if await self.dao.get_category_by_name(category_name, exclude_category_id):
            raise CategoryAlreadyExistsError(category_name)

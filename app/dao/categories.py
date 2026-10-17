from dishka import Scope
from orderflow_core.di import injectable
from sqlalchemy import Delete, Insert, Update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.categories import CreateCategoryDto, UpdateCategoryDto
from app.models.category import Category


@injectable(scope=Scope.REQUEST)
class CategoriesDao:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_categories(self) -> list[Category]:
        stmt = select(Category)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_category_by_id(self, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.category_id == category_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_category_by_name(self, category_name: str, exclude_category_id: int | None = None) -> Category | None:
        stmt = select(Category).where(Category.name == category_name)
        if exclude_category_id is not None:
            stmt = stmt.where(Category.category_id != exclude_category_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().one_or_none()

    async def create_category(self, payload: CreateCategoryDto) -> Category:
        stmt = (
            Insert(Category)
            .values(
                name=payload.name,
                description=payload.description,
            )
            .returning(Category)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.commit()

        return result.scalar_one()

    async def update_category(self, category_id: int, payload: UpdateCategoryDto) -> Category:
        stmt = (
            Update(Category)
            .where(Category.category_id == category_id)
            .values(
                name=payload.name,
                description=payload.description,
            )
            .returning(Category)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.commit()

        return result.scalar_one()

    async def delete_category(self, category_id: int) -> None:
        stmt = Delete(Category).where(Category.category_id == category_id)
        await self.db_session.execute(stmt)
        await self.db_session.commit()

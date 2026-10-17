from dishka import Scope
from orderflow_core.di import injectable
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.products import CreateProductDto, UpdateProductDto
from app.models.product import Product


@injectable(scope=Scope.REQUEST)
class ProductsDao:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_products(self) -> list[Product]:
        stmt = select(Product)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_product_by_id(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.product_id == product_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_products_by_category(self, category_id: int) -> list[Product]:
        stmt = select(Product).where(Product.category_id == category_id)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_product_by_name(
        self,
        product_name: str,
        exclude_product_id: int | None = None,
    ) -> Product | None:
        stmt = select(Product).where(Product.name == product_name)

        if exclude_product_id is not None:
            stmt = stmt.where(Product.product_id != exclude_product_id)

        result = await self.db_session.execute(stmt)
        return result.scalars().one_or_none()

    async def create_product(self, payload: CreateProductDto) -> Product:
        stmt = (
            insert(Product)
            .values(
                name=payload.name,
                description=payload.description,
                category_id=payload.category_id,
                price=payload.price,
            )
            .returning(Product)
        )

        result = await self.db_session.execute(stmt)
        product = result.scalar_one()

        await self.db_session.commit()
        await self.db_session.refresh(product, attribute_names=['category'])

        return product

    async def update_product(self, product_id: int, payload: UpdateProductDto) -> Product:
        stmt = (
            update(Product)
            .values(
                name=payload.name,
                description=payload.description,
                category_id=payload.category_id,
                price=payload.price,
            )
            .where(Product.product_id == product_id)
            .returning(Product)
        )

        result = await self.db_session.execute(stmt)
        await self.db_session.commit()

        return result.scalar_one()

    async def delete_product(self, product_id: int) -> None:
        stmt = delete(Product).where(Product.product_id == product_id)

        await self.db_session.execute(stmt)
        await self.db_session.commit()

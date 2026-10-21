from decimal import Decimal
from typing import TYPE_CHECKING

from orderflow_core.database import BaseDatabaseModel
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.category import Category


class Product(BaseDatabaseModel):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(255))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id', ondelete='CASCADE'))
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    category: Mapped['Category'] = relationship(back_populates='products', lazy='selectin')

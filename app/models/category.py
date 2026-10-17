from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseDatabaseModel

if TYPE_CHECKING:
    from app.models.product import Product


class Category(BaseDatabaseModel):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list['Product']] = relationship(back_populates='category', cascade='all, delete-orphan')

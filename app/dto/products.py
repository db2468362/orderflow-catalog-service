from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class BaseProductDto(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=3,
        max_length=50,
    )
    description: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )
    category_id: int = Field(
        gt=0,
    )
    price: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )


class CreateProductDto(BaseProductDto):
    pass


class UpdateProductDto(BaseProductDto):
    pass


class ReadProductDto(BaseProductDto):
    model_config = ConfigDict(from_attributes=True)

    product_id: int


class ReadProductsDto(RootModel[list[ReadProductDto]]):
    pass

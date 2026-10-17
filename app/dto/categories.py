from pydantic import BaseModel, ConfigDict, Field, RootModel


class BaseCategoryDto(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=3,
        max_length=50,
    )
    description: str = Field(
        min_length=3,
        max_length=255,
    )


class CreateCategoryDto(BaseCategoryDto):
    pass


class UpdateCategoryDto(BaseCategoryDto):
    pass


class ReadCategoryDto(BaseCategoryDto):
    model_config = ConfigDict(from_attributes=True)

    category_id: int


class ReadCategoriesDto(RootModel[list[ReadCategoryDto]]):
    pass

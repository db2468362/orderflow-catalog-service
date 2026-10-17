from orderflow_core.exceptions import ConflictError, NotFoundError


class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: int) -> None:
        self.category_id = category_id
        self.message = f'Category with ID {category_id} not found'
        super().__init__(self.message)


class CategoryAlreadyExistsError(ConflictError):
    def __init__(self, name: str) -> None:
        self.name = name
        self.message = f"Category with name '{name}' already exists"
        super().__init__(self.message)

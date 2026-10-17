from orderflow_core.exceptions import ConflictError, NotFoundError


class ProductNotFoundError(NotFoundError):
    def __init__(self, product_id: int) -> None:
        self.category_id = product_id
        self.message = f'Product with ID {product_id} not found'
        super().__init__(self.message)


class ProductAlreadyExistsError(ConflictError):
    def __init__(self, name: str) -> None:
        self.name = name
        self.message = f"Product with name '{name}' already exists"
        super().__init__(self.message)

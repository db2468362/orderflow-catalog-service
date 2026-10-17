from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from orderflow_core.di import setup_di
from orderflow_core.exceptions import register_exception_handlers
from sqlalchemy.ext.asyncio import AsyncEngine

import config  # noqa: F401
from app.dao import categories, products  # noqa: F401
from app.handlers.categories import router as category_router
from app.handlers.products import router as product_router
from app.infrastructure import database  # noqa: F401
from app.models.base import Base
from app.models.category import Category  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.services import categories as category_service  # noqa: F401
from app.services import products as product_service  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = await app.state.dishka_container.get(AsyncEngine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(product_router)
    app.include_router(category_router)
    register_exception_handlers(app)
    setup_di(app)

    return app


app = create_app()

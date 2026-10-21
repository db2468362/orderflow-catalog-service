# Repository guidance

- Python 3.13; dependencies and lockfile are managed with `uv` (`uv sync`). The `dev` group is declared in `pyproject.toml`.
- Run locally with `uv run uvicorn app.main:app --reload`; `docker compose up --build` starts the API and PostgreSQL together. DB settings (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`) are read from `.env` by `config.py`.
- The FastAPI app is `app.main:app`. It imports the injectable components before `setup_di(app)`; keep newly added DI-registered config, DAO, services, and models imported there so `orderflow_core` can discover them.
- `orderflow_core` supplies shared DI (`injectable`, `setup_di`), `BaseDatabaseModel`, the database lifespan, and exception-handler registration. Reuse these shared components rather than adding local equivalents.
- Register services and DAOs with `@injectable`; dependencies are supplied from type-annotated constructor arguments. For example:
  ```python
  @injectable(scope=Scope.REQUEST)
  class ProductsService:
      def __init__(self, product_dao: ProductsDao) -> None:
          self.product_dao = product_dao
  ```
  Import new injectable components in `app/main.py` before `setup_di(app)` so they are discovered.
- Request flow is handlers → services → DAOs → async SQLAlchemy session. Keep HTTP concerns in `app/handlers`, validation/serialization in `app/dto`, business checks in `app/services`, and database operations in `app/dao`.
- There are currently no checked-in tests or CI workflow. `pystolint` is the declared dev dependency; use `uv sync --dev` before invoking development tooling. No lint/test command is configured in the repo.

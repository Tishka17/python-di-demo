from collections.abc import Iterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from sqlite3 import connect, Connection

from dishka import (
    Provider, Scope, provide_all, provide, from_context, make_async_container, alias,
)
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from .dao import UserDAO, LinkDAO, create_tables
from .protocols import TransactionManager
from .use_cases import UserService, UserQueryService
from .view import router


@dataclass
class Config:
    db_path: str


class AllProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(Config, scope=Scope.APP)
    dao = provide_all(UserDAO, LinkDAO)

    services = provide_all(UserService, UserQueryService)

    @provide
    def connect(self, config: Config) -> Iterator[Connection]:
        c = connect(config.db_path)
        yield c
        c.close()

    transaction_manager = alias(Connection, provides=TransactionManager)


@asynccontextmanager
async def lifespan(app):
    # TODO: Replace with migrations
    async with app.state.dishka_container() as request_container:
        conn = await request_container.get(Connection)
        create_tables(conn)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

config = Config(db_path="app.db")
container = make_async_container(AllProvider(), context={Config: config})
setup_dishka(container=container, app=app)

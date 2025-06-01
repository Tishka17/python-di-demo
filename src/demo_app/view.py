from dataclasses import dataclass

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter

from .use_cases import NewUser, UserService, UserQueryService

router = APIRouter()


@dataclass
class NewUserResponse:
    user_id: int


@router.get("/users")
@inject
async def index(user_query_service: FromDishka[UserQueryService]) -> list[str]:
    return await user_query_service.list_names()


@router.post("/users")
@inject
async def create_user(
        data: NewUser,
        user_service: FromDishka[UserService]
) -> NewUserResponse:
    user_id = await user_service.create_user(data)
    return NewUserResponse(user_id)

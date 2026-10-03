from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.schemas.user import UserCreate, UserRead, UserListResponse
from app.services.user_service import UserService, UserId

router = APIRouter()

Service = Annotated[UserService, Depends()]

@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, service: Service):
    return service.create(user)


@router.get(
    "/users",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK
)
def get_all_users(
    service: Service,
    skip: int = 0,
    limit: int = 20,
    estado: str | None = None,
    name: str | None = None 
):
    return service.get_users(
        skip=skip,
        limit=limit,
        estado=estado,
        name=name
    )


@router.patch(
    "/users/{id}/change-status",
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
def change_user_status(
    id: int,
    service: Service
):
    return service.switch_status(id)
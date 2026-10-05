from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.schemas.user import UserCreate, UserRead, UserListResponse
from app.services.user_service import UserService, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

Service = Annotated[UserService, Depends()]

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, service: Service):
    return service.create(user)


@router.get(
    "/",
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
    "/{id}/change-status",
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
def change_user_status(
    id: int,
    service: Service
):
    return service.switch_status(id)


@router.put(
    "/{id}/update",
    response_model=UserRead,
    status_code=status.HTTP_200_OK
)
def update_user(
    id: int,
    data: UserUpdate,
    service: Service
):
    return service.update_user(id, data)
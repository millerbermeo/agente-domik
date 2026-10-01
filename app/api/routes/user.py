from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()

Service = Annotated[UserService, Depends()]

@router.post(
    "/usuarios",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserCreate, service: Service):
    return service.create(user)
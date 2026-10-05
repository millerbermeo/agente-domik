from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.schemas.auth import AuthRequest, AuthResponse
from app.services.auth_service import AuthService
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

Service = Annotated[AuthService, Depends()]

@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
def login(indent: AuthRequest, service: Service):

    usuario = service.login(
        email=indent.email,
        password=indent.password
    )

    token = create_access_token({
        "sub": usuario.email
    })

    return {
        "email": usuario.email,
        "access_token": token
    }
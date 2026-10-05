from typing import Annotated

from fastapi import Depends, HTTPException
from app.core.security import verify_password
from app.services.user_service import UserService


class AuthService:

    def __init__(self, user_service: Annotated[UserService, Depends()]):
        self.user_service = user_service

    def login(self, email: str, password: str):

        user =  self.user_service.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=404,
                detail= f"El usuario con correo: {email} no existe"
            )


        if not verify_password(
            password=password,
            hashed_password=user.password
            ):
                raise HTTPException(
                    status_code=401,
                    detail="Contranse incorrecta"
                )


        return user
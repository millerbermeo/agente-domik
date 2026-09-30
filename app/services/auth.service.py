from fastapi import HTTPException
from app.core.security import verify_password

def get_user(email: str):
    return {
        "id": 1,
        "email": email,
        "password": "12212121"
    }

def login(email: str, password: str):

    user =  get_user(email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail= f"El usuario con correo: {email} no existe"
        )


    if not verify_password(
        password=password,
        hashed_passsord=user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Contranse incorrecta"
            )


    return {
         "message": "Login exitoso",
         "usuario": user
    }
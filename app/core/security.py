from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import jwt

password_hash = PasswordHash.recommended()

SECRET_KEY = "clave-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_pass(password: str):
    return  password_hash.hash(password)

def verify_password(password: str, hashed_passsord: str)-> bool:
    return password_hash.verify(password, hashed_passsord)


def create_access_token(payload: dict):

    to_encode = payload.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })


    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


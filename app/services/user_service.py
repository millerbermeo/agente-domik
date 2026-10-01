from app.schemas.user import UserCreate
from app.models.user import User
from app.conexion.database import DBSession
from fastapi import HTTPException, status
from app.core.security import hash_pass

class UserService():

    def __init__(self, db: DBSession):
        self.db = db

    def create(self, user: UserCreate) -> User:

        exists = self.db.query(User).filter(
            User.email == user.email
        ).first()

        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="EL email ya se encuentra registrado"
            )

        new_user = User(
            name = user.name,
            email = user.email,
            password = hash_pass(user.password)
        )


        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)


        return new_user
        

    
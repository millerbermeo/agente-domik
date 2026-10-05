from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.conexion.database import DBSession
from fastapi import HTTPException, status
from app.core.security import hash_pass

class UserService:

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


    def get_users(
            self,
            skip: int = 0,
            limit: int = 20,
            estado: str | None = None,
            name: str | None = None,
    ):

        query = self.db.query(User)

        if estado:
            query = query.filter(User.status == estado)

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        total = query.count()

        users = (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            "items": users,
            "total": total,
            "skip": skip,
            "limit": limit
        }


    def switch_status(self, id: int) -> User:

        user = self.db.query(User).filter(
            User.id == id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuario no existe"
            )

        if user.status == "activo":
            user.status = "inactivo"
        else:
            user.status = "activo"


        self.db.commit()
        self.db.refresh(user)

        return user


    def update_user(self, id: int, data: UserUpdate) -> User:

        usuario = self.db.query(User).filter(
            User.id == id
        ).first()

        if not usuario:
            raise HTTPException(
                    status_code=404,
                    detail="El usuario no existe"
                )

        if data.name:
            usuario.name = data.name

        if data.email:
                    
            email_unique = self.db.query(User).filter(
                User.email ==  data.email,
                User.id != id
            ).first()

            if email_unique:
                raise HTTPException(
                    status_code=409,
                    detail="El email ya se encuentra registrado"
                )
            usuario.email = data.email

        if data.password:
            usuario.password = hash_pass(data.password)

        if data.status:
            usuario.status = data.status

        self.db.commit()
        self.db.refresh(usuario)

        return usuario


    def get_user_by_email(self, email: str):

        user = self.db.query(User).filter(
            User.email == email
        ).first()

        return user
        
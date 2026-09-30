from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel

class User(BaseModel):

    __tablename__ = "users"

    email: Mapped["str"] =  mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    name: Mapped["str"] = mapped_column(
        Text,
        nullable=False
    )

    password: Mapped["str"] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped["str"] = mapped_column(
        default="activo"
    )


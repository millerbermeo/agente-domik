from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.conexion.database import Base

from app.models.message import Message

class Conversation(Base):

    __tablename__ = "conversations"


    id: Mapped["int"] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    status: Mapped["str"] = mapped_column(
        String(50),
        nullable=False
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation"
    )
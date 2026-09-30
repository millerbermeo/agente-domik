from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, ForeignKey, relationship

from app.conexion.database import Base

from app.models.conversation import Conversation

class Message(Base):

    __tablename__ = "messages"


    id: Mapped["int"] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    type: Mapped["str"] = mapped_column(
        Text,
        nullable=False,
    )

    content: Mapped["str"] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped["str"] = mapped_column(
        Text,
        nullable=False
    )


    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id")
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages"
    )
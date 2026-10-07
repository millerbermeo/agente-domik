from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import MessageDirection, MessageStatus, MessageType

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Message(BaseModel):

    __tablename__ = "messages"

    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True
    )

    direction: Mapped[MessageDirection] = mapped_column(
        SAEnum(MessageDirection, native_enum=False),
        nullable=False
    )

    type: Mapped[MessageType] = mapped_column(
        SAEnum(MessageType, native_enum=False),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    media_url: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[MessageStatus] = mapped_column(
        SAEnum(MessageStatus, native_enum=False),
        nullable=False,
        default=MessageStatus.SENT
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages"
    )

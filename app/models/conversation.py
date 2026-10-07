from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import ChannelType, ConversationStatus

if TYPE_CHECKING:
    from app.models.message import Message


class Conversation(BaseModel):

    __tablename__ = "conversations"

    channel: Mapped[ChannelType] = mapped_column(
        SAEnum(ChannelType, native_enum=False),
        nullable=False
    )

    external_user_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    status: Mapped[ConversationStatus] = mapped_column(
        SAEnum(ConversationStatus, native_enum=False),
        nullable=False,
        default=ConversationStatus.OPEN
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation"
    )

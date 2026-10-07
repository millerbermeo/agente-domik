import enum


class ChannelType(str, enum.Enum):
    WHATSAPP = "whatsapp"
    WEB = "web"
    TELEGRAM = "telegram"


class MessageDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    LOCATION = "location"
    OTHER = "other"


class MessageStatus(str, enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class ConversationStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"

from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.chat_service import chat

router = APIRouter()


@router.post("/messages")
def send_message(data: ChatRequest):
    return chat(data.message)
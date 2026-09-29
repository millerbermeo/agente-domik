from fastapi import APIRouter, Request, Query, HTTPException
from app.core.config import settings
from app.services.whatsapp_service import process_message, send_whatsapp_message

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.get("/webhook")
def verify_token(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge")
):
    if hub_mode != "subscribe":
        raise HTTPException(
            status_code=400,
            detail="Invalid Mode"
        )

    if hub_verify_token != settings.whatsapp_verify_token:
        raise HTTPException(
            status_code=403,
            detail="invalid token"
        )

    return int(hub_challenge)


@router.post("/webhook")
async def receive_webhook(
    request: Request
):
    data = await request.json()

    value = data["entry"][0]["changes"][0]["value"]

    message = value["messages"][0]

    from_number = message["from"]

    response = await process_message(message)

    # await send_whatsapp_message(
    #     from_number,
    #     response
    # )
    
    return { "status" : "ok" }



from fastapi import APIRouter, HTTPException, Request
from app.services.calendar_service import GooggleCalendarSerivce
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/google/calendar", tags=["google"])

@router.get("/login")
def google_login():

    flow = GooggleCalendarSerivce.create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    GooggleCalendarSerivce.save_code_verifier(state, flow.code_verifier)

    return RedirectResponse(authorization_url)

@router.get("/callback")
def google_callback(request: Request):

    error = request.query_params.get("error")
    if error:
        raise HTTPException(status_code=400, detail=f"Autorización de Google denegada: {error}")

    if "code" not in request.query_params:
        raise HTTPException(status_code=400, detail="Callback accedido sin código de autorización.")

    state = request.query_params.get("state")
    code_verifier = GooggleCalendarSerivce.pop_code_verifier(state) if state else None

    if not code_verifier:
        raise HTTPException(status_code=400, detail="Sesión de autorización expirada o inválida, intentá iniciar sesión de nuevo.")

    flow = GooggleCalendarSerivce.create_flow()
    flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response = str(request.url)
    )


    credentials = flow.credentials

    return {
        "message": "Google Calendar conectado correctamente",
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
    }
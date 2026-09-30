import httpx
import os

from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.services.transcriptions_service import texto_a_audio, audio_a_texto, razonar


async def send_whatsapp_message(
    phone_number: str,
    message_type: str,
    content: str
):
    url = (
        f"https://graph.facebook.com/v26.0/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }


    if message_type == "text":
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": content
            }
        }

    elif message_type == "audio":
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "audio",
            "audio": {
                # FIX: link público (StaticFiles /audios) en vez de la ruta local
                "link": f"{settings.public_base_url}/audios/{os.path.basename(content)}"
            }
        }

    elif message_type == "image":
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "image",
            "image": {
                "link": content
            }
        }

    else:
        raise ValueError(
            f"Tipo de memnsaje no soportado: {message_type}"
        )

    # FIX: timeout 30s y reintentos de conexión (el default de 5s daba ConnectTimeout hacia graph.facebook.com)
    async with httpx.AsyncClient(timeout=30, transport=httpx.AsyncHTTPTransport(retries=2)) as client:
        response = await client.post(
            url,
            headers=headers,
            json=data
        )

    # FIX: mostrar el detalle del error de Meta (el 400 sin body no dice la causa)
    if response.is_error:
        print(f"WhatsApp API {response.status_code}: {response.text}")

    response.raise_for_status()

    return response.json()


async def process_message(message: dict):


    if message["type"] == "text":

        texto = message["text"]["body"]

        # FIX: texto entrante -> respuesta en texto (razonar), sin generar audio
        respuesta = await razonar(texto)

        return {
            "type": "text",
            "content": respuesta
        }

    if message["type"] == "audio":

        media_id = message["audio"]["id"]

        ruta_audio = await download_audio(media_id)

        texto = await audio_a_texto(ruta_audio)

        # FIX: transcribir -> razonar -> texto a audio (antes devolvía el texto transcrito como "audio")
        respuesta = await razonar(texto)
        audio = await texto_a_audio(respuesta)

        return {
            "type": "audio",
            "content": audio
        }

    return {
        "type": "text",
        "content": "Hola en que te puedo ayudar aca?"
    }


async def download_audio(media_id: str):

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}"
    }

    # Obtener información del archivo
    media_url = (
        f"https://graph.facebook.com/v26.0/"
        f"{media_id}"
    )

    # FIX: mismo timeout/reintentos al descargar el audio entrante
    async with httpx.AsyncClient(timeout=30, transport=httpx.AsyncHTTPTransport(retries=2)) as client:

        response = await client.get(
            media_url,
            headers=headers
        )

        response.raise_for_status()

        media_data = response.json()

        # URL temporal del audio
        audio_url = media_data["url"]

        # Descargar audio
        audio_response = await client.get(
            audio_url,
            headers=headers
        )

        audio_response.raise_for_status()

    # Crear carpeta
    carpeta = Path("app/audios/entrada")

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    # Nombre del archivo
    fecha = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S-%f"
    )

    ruta_audio = carpeta / f"audio_{fecha}.ogg"

    # Guardar audio
    ruta_audio.write_bytes(
        audio_response.content
    )

    return str(ruta_audio)
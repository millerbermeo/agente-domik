import httpx
from app.core.config import settings
from app.services.transcriptions_service import razonar, texto_a_audio

async def send_whatsapp_message(
        phone_number: str,
        message: str
):
    url = (
        f"https://graph.facebook.com/v26.0/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=data
        )
        
    response.raise_for_status()

    return response.json()



async def process_message(message: dict):


    print(message)

    if message["type"] == "text":

        pregunta = message["text"]["body"]
        respuesta = await (pregunta)
        ruta_audio = await texto_a_audio(respuesta)      
          
        return f"Cuentame que necesitas?"


    if message["type"] == "audio":
        media_url = message["audio"]["id"]


        # texto = await audio_a_texto(ruta_local)
        # respuesta = await razonar(texto)
        # return respuesta

        await download_audio(media_url)

    return f"Cuentame que necesitas?"
 


async def download_audio(media_url: str):

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"https://graph.facebook.com/v26.0/{media_url}",
            headers=headers
        )

        response.raise_for_status()

        media_data = response.json()

        audio_url = media_data["url"]

        audio_response = await client.get(
            audio_url,
            headers=headers
        )

        audio_response.raise_for_status()

        with open("audio.ogg", "wb") as file:
            file.write(audio_response.content)


    return "audio.ogg"
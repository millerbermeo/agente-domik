import os
import uuid
import asyncio
import httpx
import edge_tts
import imageio_ffmpeg
from app.core.config import settings
from datetime import datetime

GROQ_KEY = settings.groq_key
URL_STT = "https://api.groq.com/openai/v1/audio/transcriptions"
URL_CHAT = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {GROQ_KEY}"}


async def audio_a_texto(ruta: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        with open(ruta, "rb") as f:
            r = await client.post(
                URL_STT,
                headers=HEADERS,
                files={"file": (os.path.basename(ruta), f)},
                data={"model": "whisper-large-v3", "language": "es"},
            )
    r.raise_for_status()
    return r.json()["text"]


async def razonar(pregunta: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            URL_CHAT,
            headers=HEADERS,
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {"role": "system", "content": "Responde siempre en español, de forma breve."},
                    {"role": "user", "content": pregunta},
                ],
                "reasoning_effort": "medium",
                "max_completion_tokens": 2048,
            },
        )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


async def texto_a_audio(texto: str, salida: str | None = None) -> str:

    carpeta_salida = "app/audios/salida"
    os.makedirs(carpeta_salida, exist_ok=True)

    if salida is None:
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        salida = os.path.join(
            carpeta_salida,
            f"audio_{fecha}_{uuid.uuid4().hex[:8]}.mp3"
        )

    await edge_tts.Communicate(
        texto,
        "es-CO-SalomeNeural"
    ).save(salida)

    # FIX: convertir mp3 -> ogg/opus para que WhatsApp lo muestre como NOTA DE VOZ
    return await mp3_a_ogg_opus(salida)


async def mp3_a_ogg_opus(ruta_mp3: str) -> str:
    ruta_ogg = os.path.splitext(ruta_mp3)[0] + ".ogg"

    proceso = await asyncio.create_subprocess_exec(
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-y", "-i", ruta_mp3,
        "-vn", "-ac", "1", "-ar", "48000",  # mono, requisito de WhatsApp para notas de voz
        "-c:a", "libopus", "-b:a", "32k",
        ruta_ogg,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    _, err = await proceso.communicate()

    if proceso.returncode != 0:
        raise RuntimeError(f"ffmpeg falló: {err.decode(errors='ignore')[-300:]}")

    os.remove(ruta_mp3)
    return ruta_ogg
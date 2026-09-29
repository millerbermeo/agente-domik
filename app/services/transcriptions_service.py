import os
import uuid
import httpx
import edge_tts
from app.core.config import settings

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
    salida = salida or f"salida_{uuid.uuid4().hex}.mp3"
    await edge_tts.Communicate(texto, "es-CO-SalomeNeural").save(salida)
    return salida
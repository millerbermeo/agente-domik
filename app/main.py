import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes.whatsapp import router as whatsapp_router
from app.api.routes.user import router as user_router
from app.conexion.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

# FIX: servir los mp3 generados para que WhatsApp pueda descargarlos por URL pública
os.makedirs("app/audios/salida", exist_ok=True)
app.mount("/audios", StaticFiles(directory="app/audios/salida"), name="audios")

app.include_router(whatsapp_router, prefix="/api")
app.include_router(user_router, prefix="/api")
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    whatsapp_verify_token: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str
    groq_key: str

    public_base_url: str


    class Config:
        env_file = ".env"
        

settings = Settings()
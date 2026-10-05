from pydantic import Field, EmailStr, BaseModel

class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=250)


class AuthResponse(BaseModel):
    email: EmailStr
    access_token: str
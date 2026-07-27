from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    name: str
    role: str = Field(pattern="^(admin|partner)$")
    pin: str = Field(min_length=4, max_length=6, pattern=r"^\d+$")


class UserLogin(BaseModel):
    name: str
    pin: str = Field(min_length=4, max_length=6, pattern=r"^\d+$")


class TokenResponse(BaseModel):
    token: str
    role: str
    expires_at: str
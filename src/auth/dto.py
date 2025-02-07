import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationError


class AuthRequestDTO(BaseModel):
    username: str = Field(..., description="Уникальный username", examples=["<USERNAME>"])
    password: str = Field(..., description="Пароль (Минимум 6 символов)", min_length=6, examples=["123456"])


class TokensCreateResponseDTO(BaseModel):
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."], description="Токен доступа для авторизации пользователя")
    refresh_token: str = Field(..., examples=["dGhpc2lzYXJlZnJlc2h0b2tlbjEyMw==..."], description="Токен для обновления доступа пользователя")


class AuthRefreshTokenDTO(BaseModel):
    refresh_token: str = Field(..., examples=["dGhpc2lzYXJlZnJlc2h0b2tlbjEyMw==..."], description="Текущий refresh_token пользователя")

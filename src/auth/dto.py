import re

from pydantic import BaseModel, Field, field_validator, ValidationError


class AuthRequestDTO(BaseModel):
    username: str = Field(..., description="Уникальный username", examples=["<USERNAME>"])
    phone_number: str = Field(..., description="Номер телефона пользователя", examples=["+79123456789"])
    password: str = Field(..., description="Пароль (Минимум 6 символов)", min_length=6, examples=["123456"])

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        # Проверка на соответствие формату +7 и наличие 11 цифр
        if not re.fullmatch(r'^\+7\d{10}$', v):
            raise ValidationError('Номер телефона должен начинаться с +7 и содержать 11 цифр')
        return v


class TokensCreateResponseDTO(BaseModel):
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."], description="Токен доступа для авторизации пользователя")
    refresh_token: str = Field(..., examples=["dGhpc2lzYXJlZnJlc2h0b2tlbjEyMw==..."], description="Токен для обновления доступа пользователя")


class AuthRefreshTokenDTO(BaseModel):
    refresh_token: str = Field(..., examples=["dGhpc2lzYXJlZnJlc2h0b2tlbjEyMw==..."], description="Текущий refresh_token пользователя")

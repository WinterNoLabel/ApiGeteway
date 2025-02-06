import os
import sys

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class JWTSettings(BaseSettings):
    secret_key: str = Field(..., min_length=8, max_length=64, validation_alias='JWT_SECRET_KEY')
    algorithm: str = Field(..., max_length=64, validation_alias='JWT_ALGORITHM')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class AuthServiceSettings(BaseSettings):
    base_url: str = Field(..., validation_alias='AUTH_BASE_URL')
    port: int = Field(..., validation_alias='AUTH_PORT')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class PersonalAccountServiceSettings(BaseSettings):
    base_url: str = Field(..., validation_alias='AUTH_BASE_URL')
    port: int = Field(..., validation_alias='AUTH_PORT')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class Settings(BaseSettings):
    jwt_settings: JWTSettings = JWTSettings()
    auth_service_settings: AuthServiceSettings = AuthServiceSettings()
    personal_account_service_settings: PersonalAccountServiceSettings = PersonalAccountServiceSettings()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


settings = Settings(_env_file='../../.env')

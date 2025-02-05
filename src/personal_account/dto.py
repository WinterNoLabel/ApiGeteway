from typing import Optional

from pydantic import BaseModel, Field

class PersonalAccountResponse(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор"
    )
    username: str = Field(
        ..., description="Уникальный имя пользователя"
    )
    first_name: Optional[str] = Field(
        None, description="Имя пользователя"
    )
    photo_url: Optional[str] = Field(
        None, description="Ссылка на фотографию"
    )

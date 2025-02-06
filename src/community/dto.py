from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CommunityResponseDTO(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор"
    )
    name: str = Field(
        ..., description="Имя сообщества"
    )
    description: str = Field(
        ..., description="Описание сообщества"
    )
    creator_id: int = Field(
        ..., description="Уникальный идентификатор создателя"
    )


class CommunityRequestDTO(BaseModel):
    name: str = Field(
        ..., description="Имя сообщества"
    )
    description: str = Field(
        ..., description="Описание сообщества"
    )


class CommunityRequestToServiceDTO(BaseModel):
    name: str = Field(
        ..., description="Имя сообщества"
    )
    description: str = Field(
        ..., description="Описание сообщества"
    )
    creatorId: int = Field(
        ..., description="Уникальный идентификатор пользователя"
    )

class CreateRoleRequestDTO(BaseModel):
    name: str = Field(
        ..., description="Роль, пользователь задает ее сам"
    )
    permissions: List[int] = Field(
        ..., description="Список прав для данной роли"
    )

class CommunityResponseToServiceDTO(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор"
    )
    name: str = Field(
        ..., description="Имя сообщества"
    )
    description: str = Field(
        ..., description="Описание сообщества"
    )
    creator_id: int = Field(
        ..., description="Уникальный идентификатор пользователя"
    )
    created_at: datetime = Field(
        ..., description="Время и дата создание"
    )
    deleted_at: Optional[datetime] = Field(
        None, description="Время и дата удаление ОПЦИОНАЛЬНО"
    )

class PermissionResponseToServiceDTO(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор"
    )
    type: str = Field(
        ..., description="Тип прав"
    )

class CreateRoleResponseToServiceDTO(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор"
    )
    name: str = Field(
        ..., description="Роль, пользователь задает ее сам"
    )
    community: CommunityResponseToServiceDTO = Field(
        ..., description="Сообщество"
    )
    permissions: List[PermissionResponseToServiceDTO] = Field(
        ..., description="Права пользователя"
    )


class RevokeAndAssignRoleRequestDTO(BaseModel):
    targetUserId: int = Field(
        ..., description="ID пользователя"
    )
    roleId: int = Field(
        ..., description="ID роли"
    )


class CommunityLocationRequestDTO(BaseModel):
    locationType: str = Field(
        ..., description="Тип локации"
    )
    locationId: int = Field(
        ..., description="ID локации"
    )
    communityId: int = Field(
        ..., description="ID сообщества"
    )

class CommunityLocationResponseDTO(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор"
    )
    locationType: str = Field(
        ..., description="Тип локации"
    )
    locationId: int = Field(
        ..., description="ID локации"
    )
    communityId: int = Field(
        ..., description="ID сообщества"
    )

# class CommunityEventsResponseDTO(BaseModel):

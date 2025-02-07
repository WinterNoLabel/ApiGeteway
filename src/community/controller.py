import json
import aiohttp
from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from community.dto import CommunityResponseDTO, CommunityRequestDTO, CommunityRequestToServiceDTO, \
    CreateRoleResponseToServiceDTO, CreateRoleRequestDTO, CommunityResponseToServiceDTO, PermissionResponseToServiceDTO, \
    RevokeAndAssignRoleRequestDTO, CommunityLocationResponseDTO
from core.settings import settings
from dependency.current_user import get_user_from_token
from typing import Annotated, List


c_router = APIRouter(
    tags=["Сообщества"]
)

@c_router.get(
    "/community",
    summary="Поиск сообществ",
    status_code=status.HTTP_200_OK,
    response_model=List[CommunityResponseDTO]
)
async def search_community_send_request_to_service(current_user: Annotated[dict, Depends(get_user_from_token)],
                                                   is_owner: bool = Query(False, description="Флаг для сообществ"),
                                                   community_id: int = Query(None, description="Уникальный идентификатор сообщества"),
                                                   name: str = Query(None, description="Имя сообщества"),
                                                   description: str = Query(None, description="Описание сообщества")):
    user_id = current_user.get("id")
    url = f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community"
    headers = {
        "Content-Type": "application/json",
    }
    params = {}

    if community_id:
        params['id'] = community_id

    if name:
        params['name'] = name

    if description:
        params['description'] = description

    if is_owner:
        params['creatorId'] = user_id

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            params=params,
            headers=headers,
            ssl=False,
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=response.content,
                )

            responses = await response.json()
            return [CommunityResponseDTO(
                id=response.get("id"),
                name=response.get("name"),
                description=response.get("description"),
                creator_id=response.get("creatorId")
            ) for response in responses]


@c_router.post(
    "/community",
    summary="Создание сообщества",
    status_code=status.HTTP_201_CREATED,
    response_model=CommunityResponseDTO
)
async def create_community_send_request_to_service(current_user: Annotated[dict, Depends(get_user_from_token)],
                                                   data: CommunityRequestDTO):
    user_id = current_user.get("id")

    url = f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community"
    headers = {
        "Content-Type": "application/json",
    }

    send_data = CommunityRequestToServiceDTO(
        name=data.name,
        description=data.description,
        creatorId=user_id
    ).dict()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url,
            data=json.dumps(send_data),
            headers=headers,
            ssl=False,
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=response.content
                )

            responses = await response.json()
            return CommunityResponseDTO(
                id=responses.get("id"),
                name=responses.get("name"),
                description=responses.get("description"),
                creator_id=responses.get("creatorId")
            )

@c_router.post(
    "/community/{community_id}/roles",
    summary="Создание роли",
    status_code=status.HTTP_200_OK,
    response_model=CreateRoleResponseToServiceDTO
)
async def create_community_role_send_request_to_service(community_id: int,
                                                        current_user: Annotated[dict, Depends(get_user_from_token)],
                                                        data: CreateRoleRequestDTO):
    user_id = current_user.get("id")

    url = f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community/{community_id}/roles?userId={user_id}"

    headers = {
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url,
            headers=headers,
            data=json.dumps(data.dict()),
            ssl=False,
        ) as response:

            if response.status == 403:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="У вас нет прав"
                )
            response = await response.json()
            return CreateRoleResponseToServiceDTO(
                id=response.get("id"),
                name=response.get("name"),
                community=CommunityResponseToServiceDTO(
                    id=response.get("community").get("id"),
                    name=response.get("community").get("name"),
                    creator_id=response.get("community").get("creatorId"),
                    description=response.get("community").get("description"),
                    created_at=response.get("community").get("createdAt"),
                    deleted_at=response.get("community").get("deletedAt"),
                ),
                permissions=[PermissionResponseToServiceDTO(
                    id=permission.get("id"),
                    type=permission.get("type"),
                ) for permission in response.get("permissions")]
            )


@c_router.post(
    "/community/{community_id}/roles/revoke",
    summary="Отозвать роль у пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke_role_send_request_to_service(current_user: Annotated[dict, Depends(get_user_from_token)],
                                              community_id: int,
                                              data: RevokeAndAssignRoleRequestDTO):
    user_id = current_user.get("id")
    headers = {
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community/{community_id}/roles/revoke?userId={user_id}",
            headers=headers,
            ssl=False,
            data=json.dumps(data.dict()),
        ) as response:
            if response.status == 403 or response.status == 404:
                raise HTTPException(
                    status_code=response.status,
                    detail="Недостаточно прав" if response.status == 403 else "Связь не найдена"
                )


@c_router.post(
    "/community/{community_id}/roles/assign",
    status_code=status.HTTP_200_OK,
    summary="Назначить роль пользователю",

)
async def assign_role_send_request_to_service(current_user: Annotated[dict, Depends(get_user_from_token)],
                                              community_id: int,
                                              data: RevokeAndAssignRoleRequestDTO):

    user_id = current_user.get("id")
    headers = {
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community/{community_id}/roles/assign?userId={user_id}",
                headers=headers,
                ssl=False,
                data=json.dumps(data.dict()),
        ) as response:
            if response.status == 403 or response.status == 404:
                raise HTTPException(
                    status_code=response.status,
                    detail="Недостаточно прав" if response.status == 403 else "Связь не найдена"
                )
            if response.status == 409:
                raise HTTPException(
                    status_code=response.status,
                    detail="Роль уже назначена пользователю"
                )


@c_router.post(
    "/community/{community_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить роль"
)
async def delete_role_send_request_to_service(community_id: int,
                                              role_id: int,
                                              current_user: Annotated[dict, Depends(get_user_from_token)]):
    user_id = current_user.get("id")
    headers = {
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            url=f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community/{community_id}/roles/{role_id}?userId={user_id}",
            headers=headers,
            ssl=False,
        ) as response:
            if response.status == 403 or response.status == 404:
                raise HTTPException(
                    status_code=response.status,
                    detail="Недостаточно прав" if response.status == 403 else "Роль не найдена"
                )


@c_router.post(
    "/community-location",
    status_code=status.HTTP_200_OK,
    summary="Привязать сообщество к местоположению",
    response_model=CommunityLocationResponseDTO
)
async def community_location_send_request_to_service(current_user: Annotated[dict, Depends(get_user_from_token)]):
    user_id = current_user.get("id")
    headers = {
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community-location",
            headers=headers,
            ssl=False,
        ) as response:
            if response.status == 400:
                raise HTTPException(
                    status_code=response.status,
                    detail="Ошибка валидации"
                )

            response = await response.json()

            return CommunityLocationResponseDTO(
                id=response.get("id"),
                locationType=response.get("locationType"),
                locationId=response.get("locationId"),
                communityId=response.get("communityId"),
            )

@c_router.get(
    "/community-location/{community_id}",
    summary="Поиск местоположение сообщества по ID",
    status_code=status.HTTP_200_OK,
    response_model=CommunityLocationResponseDTO
)
async def get_community_location_send_request_to_service(community_id: int,
                                                         current_user: Annotated[dict, Depends(get_user_from_token)]):
    user_id = current_user.get("id")
    headers = {
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://{settings.community_service_settings.base_url}:{settings.community_service_settings.port}/community-location/{community_id}",
            headers=headers,
            ssl=False,
        ) as response:

            if response.status == 404:
                raise HTTPException(
                    status_code=response.status,
                    detail="Не найдено по данному ID"
                )
            response = await response.json()
            return CommunityLocationResponseDTO(
                id=response.get("id"),
                locationType=response.get("locationType"),
                locationId=response.get("locationId"),
                communityId=response.get("communityId"),
            )

# @c_router.get(
#     "/community/{community_id}/events",
#     summary="Получить список событий",
#     status_code=status.HTTP_200_OK,
#     response_model=CommunityLocationResponseDTO
# )

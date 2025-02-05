import json
from urllib import response

import aiohttp
from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from community.dto import CommunityResponseDTO, CommunityRequestDTO, CommunityRequestToServiceDTO, \
    CreateRoleResponseToServiceDTO, CreateRoleRequestDTO, CommunityResponseToServiceDTO, PermissionResponseToServiceDTO
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
    url = "https://2046-185-26-96-103.ngrok-free.app/community"
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

    url = "https://2046-185-26-96-103.ngrok-free.app/community"
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

    url = f"https://2046-185-26-96-103.ngrok-free.app/community/{community_id}/roles?userId={user_id}"

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


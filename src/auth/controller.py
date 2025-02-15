import json

from starlette import status
import aiohttp
from fastapi import APIRouter, HTTPException
from auth.dto import TokensCreateResponseDTO, AuthRequestDTO, AuthRefreshTokenDTO
from core.settings import settings

auth_router = APIRouter(
    tags=["Авторизация пользователя"],
)


@auth_router.post("/auth",
                  summary="Авторизация пользователя",
                  response_model=TokensCreateResponseDTO,
                  status_code=status.HTTP_201_CREATED
                  )
async def send_request_to_auth_service(data: AuthRequestDTO):
    json_data = json.dumps(data.dict(), ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"http://{settings.auth_service_settings.base_url}:{settings.auth_service_settings.port}/auth", headers=headers, data=json_data, ssl=False) as response:

            if response.status != 200:
                raise HTTPException(
                    detail=f"{response.status}: {response.content}",
                    status_code=response.status
                )

            return await response.json()


@auth_router.post('/refresh_token',
                  summary="Обновление токена авторизации",
                  status_code=status.HTTP_200_OK,
                  response_model=TokensCreateResponseDTO
                  )
async def send_request_to_refresh_token(data: AuthRefreshTokenDTO):
    json_data = json.dumps(data.dict(), ensure_ascii=False).encode("utf-8")

    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        async with session.post(url=f"http://{settings.auth_service_settings.base_url}:{settings.auth_service_settings.port}/refresh_token", headers=headers, data=json_data, ssl=False) as response:

            if response.status != 200:
                raise HTTPException(
                    detail=f"{response.status}: {response.content}",
                    status_code=response.status
                )

            return await response.json()

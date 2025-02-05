import json

from starlette import status
import aiohttp
from fastapi import APIRouter, HTTPException
from auth.dto import TokensCreateResponseDTO, AuthRequestDTO, AuthRefreshTokenDTO

auth_router = APIRouter(
    prefix="/api",
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
        async with session.post(url="http://127.0.0.1:8001/auth", headers=headers, data=json_data, ssl=False) as response:

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
        async with session.post(url="http://127.0.0.1:8000/refresh_token", headers=headers, data=json_data, ssl=False) as response:

            if response.status != 200:
                raise HTTPException(
                    detail=f"{response.status}: {response.content}",
                    status_code=response.status
                )

            return await response.json()

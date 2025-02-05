import aiohttp
from typing import Annotated

from starlette import status
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from dependency.current_user import get_user_from_token
from personal_account.dto import PersonalAccountResponse

pa_router = APIRouter(
    prefix="/api",
    tags=["Личный кабинет пользователя"],
)

@pa_router.get(
    "/profile",
    response_model=PersonalAccountResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает информацию о пользователе"
)
async def send_request_to_profile_service(current_user: Annotated[dict, Depends(get_user_from_token)]):
    user_id = current_user.get("id")
    headers = {"Content-Type": "application/json"}

    async with (aiohttp.ClientSession() as session):
        async with session.get(url=f"http://127.0.0.1:8080/profile?userID={user_id}",
                                headers=headers, ssl=False) as response:
            response = await response.json()

            if response.get("status"):
                raise HTTPException(
                    status_code=response.get("status"),
                    detail=response.get("detail"),
                )

            return PersonalAccountResponse(
                id=response.get("id"),
                username=response.get("username"),
                first_name=response.get("firstName"),
                photo_url=response.get("photoUrl"),
            )


@pa_router.patch(
    "/profile",
    response_model=PersonalAccountResponse,
    status_code=status.HTTP_200_OK,
    summary="Частичное обновление данных"
)
async def send_request_to_profile_service_for_partial_update(current_user: Annotated[dict, Depends(get_user_from_token)],
                                                             username: str = Form(None, description="Username пользователя"),
                                                             first_name: str = Form(None, description="Имя пользователя"),
                                                             photo: UploadFile = File(None, description="Фотография пользователя")):

    user_id = current_user.get("id")

    form_data = aiohttp.FormData()
    form_data.add_field("userID", str(user_id))

    if username:
        form_data.add_field("username", username)
    if first_name:
        form_data.add_field("firstName", first_name)
    if photo:
        form_data.add_field("photo", photo.file, filename=photo.filename, content_type=photo.content_type)

    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f"http://127.0.0.1:8080/profile", data=form_data, ssl=False) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail=response.content,
                )

            response = await response.json()

            return PersonalAccountResponse(
                id=response.get("id"),
                username=response.get("username"),
                first_name=response.get("firstName"),
                photo_url=response.get("photoUrl"),
            )

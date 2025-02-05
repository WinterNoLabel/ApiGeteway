from fastapi import FastAPI
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from auth.controller import auth_router
from personal_account.controller import pa_router
from community.controller import c_router

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

app = FastAPI(
    title="API Gateway",
    description="API Gateway",
    version="0.1.0",
    docs_url="/docs",
    root_path="/api",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(auth_router)
app.include_router(pa_router)
app.include_router(c_router)

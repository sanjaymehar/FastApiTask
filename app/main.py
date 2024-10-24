from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1 import api

app = FastAPI(
        title="Employee Management System",
        description="Employee Management System",
        docs_url="/",
        swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
        openapi_url="/openapi.json",
    )


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api.init_api_v1(app)




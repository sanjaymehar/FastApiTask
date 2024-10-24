from fastapi import FastAPI, APIRouter
from app.api.api_v1.endpoints import (
    user_base_url, user_router,
    employee_base_url, employee_router,
    salaries_base_url, salaries_router
)
from app.utils.constants import BASE_URL_V1


def init_api_v1(app: FastAPI):
    base_router_v1 = APIRouter(prefix=BASE_URL_V1)

    app.include_router(
        router=user_router,
        tags=["User"],
        prefix=user_base_url,
    )
    base_router_v1.include_router(
        router=employee_router,
        tags=["Employee"],
        prefix=employee_base_url,
    )
    base_router_v1.include_router(
        router=salaries_router,
        tags=["Salary"],
        prefix=salaries_base_url,
    )

    app.include_router(base_router_v1)

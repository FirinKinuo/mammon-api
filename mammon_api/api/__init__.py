from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette.middleware.cors import CORSMiddleware

import project
from mammon_api.settings import config
from mammon_api.api.replenishment import endpoints as replenishment_endpoints


api_router = APIRouter(prefix='/api/v1')
api_router.include_router(router=replenishment_endpoints.router)


def create_application() -> FastAPI:
    application = FastAPI(
        title="Mammon UNIT API",
        description=project.DESCRIPTION,
        version=project.VERSION,
        contact={
            'mail': project.EMAIL,
            'telegram': project.TELEGRAM
        },
        debug=config.DEBUG,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(router=api_router)

    return application


app = create_application()

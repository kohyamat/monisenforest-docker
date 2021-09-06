from typing import Any

import orjson
from app.api.routers import router as api_router
from app.api.routers.upload_file import DataExistsException
from app.core import config, tasks
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


def get_application():
    app = FastAPI(
        title=config.PROJECT_NAME,
        version=config.VERSION,
        default_response_class=ORJSONResponse,
        # docs_url='/api/docs',
        # redoc_url='/api/redoc',
        # openapi_url='/api/openapi.json'
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.include_router(api_router)
    app.include_router(api_router, prefix="/api")

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    return app


app = get_application()


@app.exception_handler(DataExistsException)
async def data_exists_exception_handler(request: Request, exc: DataExistsException):
    return JSONResponse(
        status_code=400,
        content={
            "message": f"'{exc.data['plot_id']}:{exc.data['dtype']}' already exists.",
            "id": exc.id,
            "data": exc.data,
        },
    )

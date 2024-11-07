import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

import api
from logger import logger
import config

OPEN_POSITION_PORT = config.get("OPEN_POSITION_PORT")

app = FastAPI(
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)


@app.get("/api/ping")
def ping():
    return "pong"


@app.on_event("startup")
async def app_startup():
    logger.info("On startup")
    await logger.complete()


api.include_routers(app)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="mm-tradebot API",
        version="1.0.0",
        summary="Помогайте фронтендерам",
        description="Хотелось бы верить, что эта API имеет место быть и мы не выстрелилт себе в колено",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import os

    current_directory = os.getcwd()
    print(f"Текущая директория: {current_directory}")

    uvicorn.run("main:app", host="0.0.0.0", port=OPEN_POSITION_PORT)

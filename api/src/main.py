import logging
from fastapi import FastAPI
import uvicorn
from config.settings import settings
from config.loger_config import loger_init

from parsers.handlers import router as pars_router

loger_init()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Shelfy WEB API",
    version=settings.app_version,
    redoc_url=None,
    docs_url=settings.app_swagger_url,
    root_path=settings.app_root_path,
)


app.include_router(pars_router, tags=["Парсер"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

import logging
from fastapi import FastAPI
import uvicorn

from parsers.handlers import router as pars_router

logger = logging.getLogger(__name__)


app = FastAPI(
    title="WEB API",
)


app.include_router(pars_router, tags=["Парсер"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

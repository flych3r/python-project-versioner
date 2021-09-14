from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import __version__
from app.dependencies.config import SETTINGS
from app.routers import projects
from app.utils.exceptions import BadRequestException

root_path = f'/{SETTINGS.app_env}'
app = FastAPI(
    title='MagPy API',
    description='A Rest API to manage Python projects packages versioning.',
    version=__version__,
    root_path=root_path
)
app.include_router(projects.router)


@app.exception_handler(BadRequestException)
async def unicorn_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.code,
        content={'error': exc.message},
    )


@app.get('/')
def root():
    return {'status': 'ok'}

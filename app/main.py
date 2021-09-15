from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import __version__
from app.routers import projects
from app.utils.exceptions import BadRequestError

app = FastAPI(
    title='MagPy API',
    description='A Rest API to manage Python projects packages versioning.',
    version=__version__,
)
app.include_router(projects.router)


@app.exception_handler(BadRequestError)
async def unicorn_exception_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=exc.code,
        content={'error': exc.message},
    )


@app.get('/')
def root():
    return {'status': 'ok'}

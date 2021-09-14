from fastapi import FastAPI

from app import __version__
from app.dependencies.config import SETTINGS
from app.routers import projects

root_path = f'/{SETTINGS.app_env}'
app = FastAPI(
    title='MagPy API',
    description='A Rest API to manage Python projects packages versioning.',
    version=__version__,
    root_path=root_path
)
app.include_router(projects.router)


@app.get('/')
def root():
    return {'status': 'ok'}

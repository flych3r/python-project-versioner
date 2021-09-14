from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import __version__, crud, schemas
from app.dependencies.config import SETTINGS
from app.dependencies.database import SessionLocal

root_path = f'/{SETTINGS.app_env}'
app = FastAPI(
    title='MagPy API',
    description='A Rest API to manage Python projects packages versioning.',
    version=__version__,
    root_path=root_path
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/projects/', response_model=List[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return projects


@app.get('/projects/{project_name}', response_model=schemas.Project)
def get_project_detail(project_name: str, db: Session = Depends(get_db)):
    # TODO
    # - Retornar informações do projeto
    return {'foo': 'bar'}


@app.post('/projects/', response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # TODO
    # - Processar pacotes recebidos
    # - Persistir as informações no banco
    return {'foo': 'bar'}


@app.delete('/projects/{project_id}')
def delete_project(project_name: str, db: Session = Depends(get_db)):
    # TODO
    # - Apagar o projeto indicado
    return {'foo': 'bar'}

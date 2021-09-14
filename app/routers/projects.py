from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies.database import get_db

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.get('/', response_model=List[schemas.ProjectView])
def get_projects(db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return [
        schemas.ProjectView(name=p.name, packages=p.packages_releases)
        for p in projects
    ]


@router.get('/{project_name}', response_model=schemas.Project)
def get_project_detail(project_name: str, db: Session = Depends(get_db)):
    # TODO
    # - Retornar informações do projeto
    return crud.get_project(db, project_name.lower().replace('-', '_'))


@router.post('/', response_model=schemas.Project)
def create_project(project: schemas.ProjectView, db: Session = Depends(get_db)):
    # TODO
    # - Processar pacotes recebidos
    # - Persistir as informações no banco
    return crud.create_project(db, project)


@router.delete('/{project_id}')
def delete_project(project_name: str, db: Session = Depends(get_db)):
    # TODO
    # - Apagar o projeto indicado
    return {'foo': 'bar'}

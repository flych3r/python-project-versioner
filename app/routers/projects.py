from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies.database import get_db
from app.utils.exceptions import BadRequestException, ExceptionModel
from app.utils.pypi import check_package_version

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.get('/', response_model=List[schemas.ProjectView])
def get_projects(db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return [
        {'name': p.name, 'packages': p.packages_releases}
        for p in projects
    ]


@router.get(
    '/{project_name}/',
    response_model=schemas.ProjectView,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ExceptionModel}}
)
def get_project_detail(project_name: str, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_name)
    if project is None:
        raise BadRequestException(message='Project not found')
    return {'name': project.name, 'packages': project.packages_releases}


@router.post(
    '/',
    response_model=schemas.ProjectView, status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ExceptionModel}}
)
def create_project(project: schemas.ProjectView, db: Session = Depends(get_db)):
    project.packages = [*map(check_package_version, project.packages)]
    project_db = crud.create_project(db, project)
    return {'name': project_db.name, 'packages': project_db.packages_releases}


@router.delete(
    '/{project_name}/',
    responses={
        status.HTTP_200_OK: {'message': 'str'},
        status.HTTP_400_BAD_REQUEST: {'model': ExceptionModel}
    }
)
def delete_project(project_name: str, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_name)
    if project is None:
        raise BadRequestException(message='Project not found')
    _ = crud.delete_project(db, project)
    return {'message': 'Project deleted'}

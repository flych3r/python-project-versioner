from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies.database import get_db
from app.utils.exceptions import BadRequestError, ExceptionModel
from app.utils.pypi import check_package_version, normalize

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
)


@router.get('/', response_model=List[schemas.ProjectView])
def get_projects(db: Session = Depends(get_db)):
    """Fetches all projects from the database."""
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
    """Fetches one project from the database by name."""
    project = crud.get_project(db, project_name)
    if project is None:
        raise BadRequestError(message='Project not found')
    return {'name': project.name, 'packages': project.packages_releases}


@router.post(
    '/',
    response_model=schemas.ProjectView, status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {'model': ExceptionModel}}
)
def create_project(project: schemas.ProjectView, db: Session = Depends(get_db)):
    """Adds a new project to the database."""
    pkg_names = [pkg.name for pkg in project.packages]
    if len(set(map(normalize, pkg_names))) < len(pkg_names):
        raise BadRequestError(message='One or more packages are duplicated')
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
    """Removes a project from the database."""
    project = crud.get_project(db, project_name)
    if project is None:
        raise BadRequestError(message='Project not found')
    _ = crud.delete_project(db, project)
    return {'message': 'Project deleted'}

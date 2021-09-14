from typing import List

from fastapi import APIRouter, Depends, status
from requests.exceptions import HTTPError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud, schemas
from app.dependencies.database import get_db
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


@router.get('/{project_name}', response_model=schemas.ProjectView)
def get_project_detail(project_name: str, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_name)
    return {'name': project.name, 'packages': project.packages_releases}


@router.post(
    '/',
    response_model=schemas.ProjectView, status_code=status.HTTP_201_CREATED,
    responses={400: {'model': schemas.PyPiException}}
)
def create_project(project: schemas.ProjectView, db: Session = Depends(get_db)):
    try:
        project.packages = [*map(check_package_version, project.packages)]
        project_db = crud.create_project(db, project)
    except HTTPError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': "One or more packages doesn't exist"},
        )
    return {'name': project_db.name, 'packages': project_db.packages_releases}


@router.delete('/{project_name}')
def delete_project(project_name: str, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_name)
    return crud.delete_project(db, project)

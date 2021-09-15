from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.exceptions import BadRequestError
from app.utils.pypi import normalize


def get_projects(db: Session) -> List[models.Project]:
    """
    Fetches all projects on the database.

    Parameters
    ----------
    db : Session
        database session

    Returns
    -------
    list of Project
        projects on table
    """
    return db.query(models.Project).all()


def get_project(db: Session, project_name: str) -> Optional[models.Project]:
    """
    Fetches one Project from the database by name.

    Parameters
    ----------
    db : Session
        database session
    project_name : str
        name of the project

    Returns
    -------
    Project or None
        project if exists on table
    """
    return db.query(models.Project).filter(
        models.Project.normalized_name == normalize(project_name)
    ).first()


def create_project(db: Session, project: schemas.ProjectView) -> models.Project:
    """
    Inserts a new project on the database.

    Parameters
    ----------
    db : Session
        database session
    project : ProjectView
        project to insert

    Returns
    -------
    Project
        new added project

    Raises
    ------
    BadRequestError
        If the project is already in the database
    """
    try:
        db_project = models.Project(
            name=project.name,
            normalized_name=normalize(project.name),
            packages_releases=[
                models.PackageRelease(name=pkg.name, version=pkg.version)
                for pkg in project.packages
            ]
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except IntegrityError:
        raise BadRequestError(message='Project already exists')


def get_packages_releases(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.PackageRelease]:
    """
    Fetches all packages from the database.

    Parameters
    ----------
    db : Session
        database session
    skip : int, optional
        number of rows to skip, by default 0
    limit : int, optional
        number of rows to fetch , by default 100

    Returns
    -------
    list of packages
        packages on the database by page
    """
    return db.query(models.PackageRelease).offset(skip).limit(limit).all()


def delete_project(db: Session, project: models.Project) -> bool:
    """
    Removes a project from the database.

    Parameters
    ----------
    db : Session
        database session
    project : Project
        project to delete

    Returns
    -------
    bool
        project was deleted
    """
    db.delete(project)
    db.commit()
    return True

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.exceptions import BadRequestException
from app.utils.pypi import normalize


def get_projects(db: Session):
    return db.query(models.Project).all()


def get_project(db: Session, project_name: str):
    return db.query(models.Project).filter(
        models.Project.normalized_name == normalize(project_name)
    ).first()


def create_project(db: Session, project: schemas.ProjectView):
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
        raise BadRequestException(message='Project already exists')


def get_packages_releases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PackageRelease).offset(skip).limit(limit).all()


def delete_project(db: Session, project: models.Project):
    db.delete(project)
    db.commit()
    return True

from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.pypi import normalize


def get_projects(db: Session):
    return db.query(models.Project).all()


def get_project(db: Session, project_id: str):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def create_project(db: Session, project: schemas.ProjectView):
    db_project = models.Project(
        id=normalize(project.name),
        name=project.name,
        packages_releases=[
            models.PackageRelease(name=pkg.name, version=pkg.version)
            for pkg in project.packages
        ]
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_packages_releases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PackageRelease).offset(skip).limit(limit).all()


def delete_project(db: Session, project: models.Project):
    db.delete(project)
    db.commit()
    return {'message': 'Project deleted'}

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.dependencies.database import Base


class Project(Base):
    """
    ORM model for a project.

    Parameters
    ----------
        id: int, primary_key
            uid of the project
        name: str
            name of the project
        normalized_name: str, unique
            unique name for the project
        package_releases: list of PackageRelease, relationship
            packages associated with the project
    """

    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    normalized_name = Column(String, unique=True, index=True)

    packages_releases = relationship('PackageRelease', back_populates='project')


class PackageRelease(Base):
    """
    ORM model for a package.

    Parameters
    ----------
        id: int, primary_key
            uid of the project
        name: str
            name of the package
        version: str
            version of the package
        project_id: int, foreign_key
            id of the project associated with the package
        project: Project, relationship
            project with the package
    """

    __tablename__ = 'packages_releases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    version = Column(String, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship('Project', back_populates='packages_releases')

from typing import List, Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

from app import models


class PackageReleaseBase(BaseModel):
    """Base model for a package."""

    name: str
    version: str


class PackageReleaseView(PackageReleaseBase):
    """Package with an optional version field."""

    version: Optional[str]  # type: ignore[assignment]


class PackageRelease(PackageReleaseBase):
    """Model mapping Package ORM."""

    id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    """Base model for a project."""

    name: str


class ProjectView(ProjectBase):
    """Package with packages."""

    packages: List['PackageReleaseView']

    @validator('packages', pre=True, each_item=True)
    def extract_packages(cls, value):  # noqa: N805, D102
        if isinstance(value, models.PackageRelease):
            return PackageReleaseView(name=value.name, version=value.version)
        return value


class Project(ProjectBase):
    """Model mapping Project ORM."""

    id: int
    packages_releases: List[PackageRelease] = []

    class Config:
        orm_mode = True


class PyPiException(BaseModel):
    """PyPi exception model."""

    error: str = "One or more packages doesn't exist"

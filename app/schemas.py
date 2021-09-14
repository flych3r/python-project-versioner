from typing import List, Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

from app import models


class PackageReleaseBase(BaseModel):

    name: str
    version: str


class PackageReleaseView(PackageReleaseBase):

    version: Optional[str]  # type: ignore[assignment]


class PackageRelease(PackageReleaseBase):
    id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):

    name: str


class ProjectView(ProjectBase):
    packages: List['PackageReleaseView']

    @validator('packages', pre=True, each_item=True)
    def extract_packages(cls, value):  # noqa: N805
        if isinstance(value, models.PackageRelease):
            return PackageReleaseView(name=value.name, version=value.version)
        return value


class Project(ProjectBase):
    id: int
    packages_releases: List[PackageRelease] = []

    class Config:
        orm_mode = True


class PyPiException(BaseModel):
    error: str = "One or more packages doesn't exist"

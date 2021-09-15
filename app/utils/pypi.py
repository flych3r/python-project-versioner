import re

import requests

from app.utils.exceptions import BadRequestError


def normalize(name: str) -> str:
    """
    Normalizes the name of the package.

    The name should be lowercased with all runs of the characters ., -, or _
    replaced with a single - character.
    """
    return re.sub(r'[-_.]+', '-', name).lower()


def check_package_version(package):
    """
    Validates package name and version, adding version if missing.

    Parameters
    ----------
    package : PackageRelease
        package with name and version

    Returns
    -------
    package
        validated package

    Raises
    ------
    BadRequestError
        If package doesn't exists
    """
    name = package.name
    version = package.version

    url = f'https://pypi.org/pypi/{name}/json'
    if version:
        url = f'https://pypi.org/pypi/{name}/{version}/json'
    r = requests.get(url)
    if r.ok:
        package.version = r.json().get('info').get('version')
        return package
    raise BadRequestError(message="One or more packages doesn't exist")

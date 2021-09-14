import re

import requests

from app.utils.exceptions import BadRequestException


def normalize(name):
    return re.sub(r'[-_.]+', '-', name).lower()


def check_package_version(package):
    name = package.name
    version = package.version

    url = f'https://pypi.org/pypi/{name}/json'
    if version:
        url = f'https://pypi.org/pypi/{name}/{version}/json'
    r = requests.get(url)
    if r.ok:
        package.version = r.json().get('info').get('version')
        return package
    raise BadRequestException(message="One or more packages doesn't exist")

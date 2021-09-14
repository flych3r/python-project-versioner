import re

import requests


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
    r.raise_for_status()

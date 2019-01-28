#!/usr/bin/env python

import os

try:
    from setuptools import setup, find_packages
except:
    raise Exception('setuptools is required for installation')


def join(*paths):
    """Join and normalize several paths.
    Args:
        *paths (List[str]): The paths to join and normalize.
    Returns:
        str: The normalized path.
    """

    return os.path.normpath(os.path.join(*paths))


VERSION_PATH = join(__file__, '..', 'target_finder_model', 'version.py')


def get_version():
    """Get the version number without running version.py.
    Returns:
        str: The current uavaustin-target-finder version.
    """

    with open(VERSION_PATH, 'r') as version:
        out = {}

        exec(version.read(), out)

        return out['__version__']


setup(
    name='target-finder-model',
    version=get_version(),
    author='UAV Austin',
    url='https://github.com/uavaustin/target-finder-model',
    packages=find_packages(),
    package_data={
        'target_finder_model': [
            'data/preclf-test.cfg',
            'data/yolo3detector-test.cfg'
        ]
    },
    license='MIT'
)

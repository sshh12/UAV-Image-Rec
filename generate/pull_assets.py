#!/usr/bin/env python3

import os
import shutil
import tarfile

import requests

import config


def pull_all():
    """Pull all assets."""
    pull_backgrounds()
    pull_base_shapes()
    pull_nas_images()


def pull_backgrounds():
    """Pull the shape generation backgrounds."""
    _pull_asset(config.BACKGROUNDS_URL)


def pull_base_shapes():
    """Pull the base shape images."""
    _pull_asset(config.BASE_SHAPES_URL)


def pull_nas_images():
    """Pull the images to generate not-a-shapes."""
    _pull_asset(config.NAS_IMAGES_URL)


# Fetch and extract a file from a URL.
def _pull_asset(url):
    filename = _download_file(url)
    _untar(filename)


# Download a file to the assets folder and return the filename.
def _download_file(url):
    # Make sure the assets folder exists.
    os.makedirs(config.ASSETS_DIR, exist_ok=True)

    asset = url.split('=')[-1]
    filename = os.path.join(config.ASSETS_DIR, asset)

    # If the file exists don't pull it again since it's versioned
    # and should remain constant. Otherwise, stream it to disk.
    if not os.path.isfile(filename):
        print(f'Fetching {asset}...', end='', flush=True)

        res = requests.get(url, stream=True)

        with open(filename, 'wb') as f:
            shutil.copyfileobj(res.raw, f)

        print(' done.')

    return filename


# Untar a file, unless the directory already exists.
def _untar(filename):
    dirname = filename.split('.tar.gz')[0]

    if not os.path.isdir(dirname):
        asset = os.path.basename(filename)

        print(f'Extracting {asset}...', end='', flush=True)

        shutil.unpack_archive(filename, config.ASSETS_DIR)

        print(' done.')


if __name__ == '__main__':
    pull_all()

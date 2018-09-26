"""Contains configuration settings for generation."""

import os.path


# Settings for pulling assets.

BACKGROUNDS_VERSION = 'v1'
BASE_SHAPES_VERSION = 'v1'
NAS_IMAGES_VERSION = 'v1'

DOWNLOAD_BASE = (
    'https://bintray.com/uavaustin/target-finder-assets/'
    'download_file?file_path='
)

BACKGROUNDS_URL = (
    DOWNLOAD_BASE + 'backgrounds-' + BACKGROUNDS_VERSION + '.tar.gz'
)
BASE_SHAPES_URL = (
    DOWNLOAD_BASE + 'base-shapes-' + BASE_SHAPES_VERSION + '.tar.gz'
)
NAS_IMAGES_URL = DOWNLOAD_BASE + 'nas-images-' + NAS_IMAGES_VERSION + '.tar.gz'

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

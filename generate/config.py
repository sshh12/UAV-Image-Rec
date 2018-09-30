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

BACKGROUNDS_DIR = os.path.join(ASSETS_DIR,
                               'backgrounds-' + BACKGROUNDS_VERSION)
BASE_SHAPES_DIR = os.path.join(ASSETS_DIR,
                               'base-shapes-' + BASE_SHAPES_VERSION)
NAS_IMAGES_DIR = os.path.join(ASSETS_DIR, 'nas-images-' + NAS_IMAGES_VERSION)

# Settings for shape and not-a-shape (nas) generation.

SHAPES_DIR = os.path.join(os.path.dirname(__file__), 'shapes')

NUM_SHAPES = 5000  # Number of each shape.

ALPHAS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

ALPHA_FONT_DIR = os.path.join(os.path.dirname(__file__), 'vendor', 'open-sans')
ALPHA_FONTS = [
    os.path.join(ALPHA_FONT_DIR, 'OpenSans-SemiBold.ttf'),
    os.path.join(ALPHA_FONT_DIR, 'OpenSans-Bold.ttf')
]

# The shapes to generate.
SHAPE_TYPES = [
    'circle',
    'cross',
    'pentagon',
    'quarter-circle',
    'rectangle',
    'semicircle',
    'square',
    'star',
    'trapezoid',
    'triangle'
]

SHAPE_COLORS = [
    '#407340',
    '#94ff94',
    '#00ff00',
    '#008004',
    '#525294',
    '#7f7fff',
    '#0000ff',
    '#000087',
    '#808080',
    '#994c00',
    '#e1dd68',
    '#fffc7a',
    '#fff700',
    '#d2cb00',
    '#d8ac53',
    '#FFCC65',
    '#ffa500',
    '#d28c00',
    '#bc3c3c',
    '#ff5050',
    '#ff0000',
    '#9a0000',
    '#800080'
]

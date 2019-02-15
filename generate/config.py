"""Contains configuration settings for generation."""

import os


# [Asset Settings and Files]
BACKGROUNDS_VERSION = 'v2'
BASE_SHAPES_VERSION = 'v1'

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

ASSETS_DIR = os.environ.get('ASSETS_DIR',
                            os.path.join(os.path.dirname(__file__), 'assets'))

BACKGROUNDS_DIR = os.path.join(ASSETS_DIR,
                               'backgrounds-' + BACKGROUNDS_VERSION)
BASE_SHAPES_DIR = os.path.join(ASSETS_DIR,
                               'base-shapes-' + BASE_SHAPES_VERSION)


DATA_DIR = os.environ.get('DATA_DIR',
                          os.path.join(os.path.dirname(__file__), 'data'))

# [Number of Images]
# Generate num - offset images
NUM_OFFSET = int(os.environ.get('NUM_OFFSET', '0'))
NUM_IMAGES = int(os.environ.get('NUM_IMAGES', '30'))
NUM_VAL_OFFSET = int(os.environ.get('NUM_VAL_OFFSET', '0'))
NUM_VAL_IMAGES = int(os.environ.get('NUM_VAL_IMAGES', '10'))

# Max images to generate per image
MAX_PER_SHAPE = int(os.environ.get('MAX_PER_SHAPE', '16'))

# Specify number of threads to use for shape generation. Default lets
# the multiprocessing library determine.
NUM_THREADS = int(os.environ.get('NUM_THREADS', 0))

# [Shape Specs]
SHAPE_TYPES = os.environ.get(
    'SHAPE_TYPES',
    'circle,cross,pentagon,quarter-circle,rectangle,semicircle,square,star,'
    'trapezoid,triangle'
).split(',')

CLF_TYPES = ['background', 'shape_target']

TARGET_COLORS = ['black', 'red', 'blue',
                 'green', 'yellow', 'purple', 'orange']

ALPHA_COLORS = ['white', 'black', 'gray', 'red', 'blue',
                'green', 'yellow', 'purple', 'orange']

COLORS = {
    'white': [
        (250, 250, 250)],
    'black': [
        (5, 5, 5)],
    'gray': [
        (128, 128, 128)],
    'red': [
        (188, 60, 60),
        (255, 80, 80),
        (255, 0, 0),
        (154, 0, 0)],
    'blue': [
        (0, 0, 255),
        (0, 0, 135)],
    'green': [
        (64, 115, 64),
        (148, 255, 148),
        (0, 255, 0),
        (0, 128, 4)],
    'yellow': [
        (225, 221, 104),
        (255, 252, 122),
        (255, 247, 0),
        (210, 203, 0)],
    'purple': [
        (127, 127, 255),
        (128, 0, 128)
    ],
    'orange': [
        (153, 76, 0),
        (216, 172, 83),
        (255, 204, 101),
        (255, 165, 0),
        (210, 140, 0)]
}

ALPHAS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

ALPHA_FONT_DIR = os.path.join(os.path.dirname(__file__), 'vendor', 'fonts')
ALPHA_FONTS = [
    os.path.join(ALPHA_FONT_DIR, 'Rajdhani', 'Rajdhani-Bold.ttf'),
    os.path.join(ALPHA_FONT_DIR, 'Gudea', 'Gudea-Bold.ttf'),
    os.path.join(ALPHA_FONT_DIR, 'Inconsolata', 'Inconsolata-Bold.ttf'),
    os.path.join(ALPHA_FONT_DIR, 'Open_Sans', 'OpenSans-Bold.ttf'),
    os.path.join(ALPHA_FONT_DIR, 'Open_Sans', 'OpenSans-SemiBold.ttf'),
    os.path.join(ALPHA_FONT_DIR, 'News_Cycle', 'NewsCycle-Bold.ttf')
]

# [Model Dimensions]
FULL_SIZE = (4240, 2400)
CROP_SIZE = (400, 400)
CROP_OVERLAP = 100
DETECTOR_SIZE = (608, 608)
PRECLF_SIZE = (64, 64)

# [Darknet Models]

# Whether to delete full image data when they are converted
DELETE_ON_CONVERT = False

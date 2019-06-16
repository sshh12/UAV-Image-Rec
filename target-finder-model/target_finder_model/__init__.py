"""Entrypoint for the target_finder_model library.

This module contains the filenames used for target-finder so they can
be encapsulated in a single python library that can be fetched.
"""

from pkg_resources import resource_filename

from .version import __version__


# Darknet Config
preclf_file = resource_filename(__name__, 'data/preclf-test.cfg')
yolo3_file = resource_filename(__name__, 'data/yolo3detector-test.cfg')

preclf_weights = resource_filename(__name__,
                                   'data/preclf-train_final.weights')
yolo3_weights = resource_filename(__name__,
                                  'data/yolo3detector-train_final.weights')

# Model Classes
CLF_CLASSES = ['background', 'shape_target']
YOLO_CLASSES = (
    'circle,cross,pentagon,quarter-circle,rectangle,semicircle,square,star,'
    'trapezoid,triangle'
).split(',') + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ4')

# Other Model Params (match with generate/config.py)
FULL_SIZE = (4240, 2400)
CROP_SIZE = (400, 400)
CROP_OVERLAP = 100
DETECTOR_SIZE = (608, 608)
PRECLF_SIZE = (64, 64)

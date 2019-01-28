#!/usr/bin/env python3

import multiprocessing
import os.path
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), 'generate'))


from create_full_images import generate_all_shapes


if __name__ == '__main__':
    # Make sure Windows doesn't blow up with the multiprocessing in
    # the shape generation script.
    multiprocessing.freeze_support()

    generate_all_shapes()

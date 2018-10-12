#!/usr/bin/env python3

import multiprocessing
import os.path
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), 'generate'))


from nas_gen import generate_nas
from pull_assets import pull_all
from shape_gen import generate_all_shapes
from train import train


if __name__ == '__main__':
    # Make sure Windows doesn't blow up with the multiprocessing in
    # the shape generation script.
    multiprocessing.freeze_support()

    pull_all()
    generate_nas()
    generate_all_shapes()
    train()

#!/usr/bin/env python3

import fileinput
import os
import subprocess
import sys

import config


def train():
    """Create the Tensorflow model."""
    # Make sure the data folder exists.
    os.makedirs(config.DATA_DIR, exist_ok=True)

    # Execute the retraining command for Inception V3.
    subprocess.call([
        sys.executable, config.RETRAIN_FILE,
        '--output_graph', config.GRAPH_OUTPUT,
        '--output_labels', config.LABELS_OUTPUT,
        '--bottleneck_dir', config.BOTTLENECK_DIR,
        '--image_dir', config.SHAPES_DIR,
        '--how_many_training_steps', config.TRAINING_STEPS
    ])

    # Change the labels to work with target-finder. This makes them
    # uppercase and replace spaces with underscores.
    with fileinput.input(files=config.LABELS_OUTPUT, inplace=True) as f:
        for line in f:
            print(line.replace(' ', '_').upper(), end='')


if __name__ == '__main__':
    train()

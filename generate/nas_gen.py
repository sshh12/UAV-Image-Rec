#!/usr/bin/env python3

import glob
import io
import os
import sys

import cv2
import numpy as np
from PIL import Image
from progress.bar import IncrementalBar

import config


def generate_nas():
    """Generate not-a-shapes in the shapes directory."""
    os.makedirs(os.path.join(config.SHAPES_DIR, 'nas'), exist_ok=True)

    num_shapes = 0
    filenames = _get_nas_assets()

    # Wrap this operation with a nice progress bar.
    bar = IncrementalBar('NAS Generation', max=config.NUM_SHAPES)

    # Use each file in the nas-images folder to generate blobs.
    for image in _get_all_nas_images(filenames):
        if num_shapes == config.NUM_SHAPES:
            break

        _save_image(image, num_shapes)

        num_shapes += 1
        bar.next()

    bar.finish()

    if num_shapes != config.NUM_SHAPES:
        print('Not enough NAS blobs could be created.')


# Get the NAS assets.
def _get_nas_assets():
    filenames = glob.glob(os.path.join(config.NAS_IMAGES_DIR, '*.jpg'))

    if len(filenames) == 0:
        print('NAS Assets were not found, make sure they have been fetched',
              file=sys.stderr)

        sys.exit(1)
    else:
        return filenames


# Yields images from all files.
def _get_all_nas_images(filenames):
    for filename in filenames:
        for image in _get_nas_images(filename):
            yield image


# Generator that returns blobs in an image.
def _get_nas_images(filename):
    image = Image.open(filename)

    mask_image = cv2.imread(filename)
    image_width, image_height = image.size

    # Initial edge detection.
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    edges = cv2.Canny(cv_image, 50, 200)
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, 1)
    edges = cv2.erode(edges, kernel, 1)

    ret, thresh = cv2.threshold(edges, 127, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)

    # Yield a iamge for each contour if the area and width and height
    # are appropriate after cropping.
    for cnt in contours:
        x, y, width, height = cv2.boundingRect(np.asarray(cnt))

        # Crop image to interesting shape.
        x_1 = max(x - config.NAS_PADDING, 0)
        y_1 = max(y - config.NAS_PADDING, 0)
        y_2 = min(y + height + config.NAS_PADDING, image_height)
        x_2 = min(x + width + config.NAS_PADDING, image_width)

        blob_image = mask_image[y_1:y_2, x_1:x_2]

        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        width, height = blob_image.shape[:2]

        if area < 5000 and perimeter < area / 2 and width > 30 and height > 30:
            yield blob_image


# Save an image to the output directory.
def _save_image(image, number):
    filename = os.path.join(config.SHAPES_DIR, 'nas', f'nas-{number:06d}.jpg')
    cv2.imwrite(filename, image)


if __name__ == '__main__':
    generate_nas()

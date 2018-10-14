#!/usr/bin/env python3

import glob
import multiprocessing
import os
import random
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from progress.bar import Bar
import webcolors

import config


def generate_all_shapes():
    """Generate all images for all shapes."""
    for shape in config.SHAPE_TYPES:
        generate_shapes(shape)


def generate_shapes(shape):
    """Generate shapes of a given type.

    Note that shape generation is deterministic because the random
    number generator has been seeded. However, the random variable
    state is reset to how it was before generation.

    Shapes generated between runs are always consistent, and runs are
    resumed in the same place if they are stopped midway through.

    Shapes are generated using a thread pool. By default, this will
    take nearly all processing power. To decrease this, you may set
    the NUM_THREADS environment variable.
    """
    os.makedirs(os.path.join(config.SHAPES_DIR, shape), exist_ok=True)
    existing = _get_existing(shape)

    if len(existing) > config.NUM_SHAPES:
        print(f'Clearing out excess {shape.title()} images.')

        for i in existing:
            if i >= config.NUM_SHAPES:
                _delete_image(shape, i)

        # Take out the numbers that were removed.
        existing = list(filter(lambda x: x < config.NUM_SHAPES, existing))

    if len(existing) == config.NUM_SHAPES:
        print(f'{shape.title()} image count already met, skipping generation.')
        return

    r_state = random.getstate()

    # Seed the random number generator with the shape name.
    random.seed(shape)

    # All the random selection is generated ahead of time, that way
    # the process can be resumed without the shapes changing on each
    # run.
    numbers = list(range(0, config.NUM_SHAPES))
    existing_list = [existing for i in numbers]
    shapes = [shape for i in numbers]
    bases = _random_list(_get_base_shapes(shape))
    backgrounds = _random_list(_get_backgrounds())
    background_colors = _random_list(config.SHAPE_COLORS)
    alphas = _random_list(config.ALPHAS)
    alpha_colors = _random_list(config.SHAPE_COLORS)
    font_files = _random_list(config.ALPHA_FONTS)
    sizes = _random_list(range(50, 201))
    paddings = _random_list(range(10, 31))
    angles = _random_list(range(0, 360))
    crops = _random_list(range(60, 81))
    blur_radii = _random_list(range(1, 7))

    # Put everything into one large iterable so that we can split up
    # data across thread pools.
    data = zip(numbers, existing_list, shapes, bases, backgrounds,
               background_colors, alphas, alpha_colors, font_files, sizes,
               paddings, angles, crops, blur_radii)

    random.setstate(r_state)

    num_width = str(len(str(config.NUM_SHAPES)))
    bar_suffix = '%(index)' + num_width + 'd/%(max)d [%(elapsed_td)s]'

    bar = Bar('{:25s}'.format(shape.title() + ' Generation'),
              max=config.NUM_SHAPES, suffix=bar_suffix)

    # Generate in a pool. If specificed, use a given number of
    # threads.
    with multiprocessing.Pool(config.NUM_THREADS or None) as pool:
        for i in pool.imap_unordered(_generate_single_shape, data):
            bar.next()

    bar.finish()


# One iteration in the function above, runs in a pool.
def _generate_single_shape(args):
    number = args[0]
    existing = args[1]
    shape = args[2]
    data = args[2:]

    if number not in existing:
        image = _create_shape(*data)
        _save_image(image, shape, number)


# Get the background assets. This is returned as list of images.
def _get_backgrounds():
    filenames = glob.glob(os.path.join(config.BACKGROUNDS_DIR, '*.png'))

    if len(filenames) == 0:
        print('Background assets were not found, make sure they have been '
              'fetched', file=sys.stderr)

        sys.exit(1)
    else:
        return [Image.open(filename) for filename in sorted(filenames)]


# Get the base shape assets. This is returned as list of images.
def _get_base_shapes(shape):
    filenames = glob.glob(os.path.join(config.BASE_SHAPES_DIR, shape, '*.png'))

    if len(filenames) == 0:
        print(f'Base shape assets for {shape} were not found, make sure they '
              'have been fetched', file=sys.stderr)

        sys.exit(1)
    else:
        return [Image.open(filename) for filename in sorted(filenames)]


# Get the shapes that have already been generated.
def _get_existing(shape):
    numbers = []

    for filename in glob.glob(os.path.join(config.SHAPES_DIR, shape, '*.jpg')):
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]

        numbers.append(int(name.split('-')[-1]))

    return sorted(numbers)


# Return a list with items randomly chosen.
def _random_list(items, count=config.NUM_SHAPES):
    return [random.choice(items) for i in range(0, count)]


# Create a shape given all the input parameters.
def _create_shape(shape, base, background, background_color, alpha,
                  alpha_color, font_file, size, padding, angle, crop,
                  blur_radius):
    image = _get_base(base, size)
    image = _add_background_color(image, background_color)
    image = _add_alphanumeric(image, shape, alpha, alpha_color, font_file)
    image = _rotate_shape(image, shape, size, angle, crop)
    image = _add_background(image, background, size, padding, blur_radius)
    image = image.convert('RGB')

    return image


def _get_base(base, size):
    # Start with a sized version of the base shape.
    image = base.copy()
    image.resize((size, size), 0)
    image = image.convert('RGBA')

    return image


def _add_background_color(image, background_color):
    for x in range(image.width):
        for y in range(image.height):
            pixel_color = image.getpixel((x, y))

            if pixel_color[0] == 255 and pixel_color[1] == 255 and \
                    pixel_color[2] == 255:
                image.putpixel((x, y), (255, 255, 255, 0))
            else:
                image.putpixel((x, y), webcolors.hex_to_rgb(background_color))

    return image


def _add_alphanumeric(image, shape, alpha, alpha_color, font_file):
    # Adjust alphanumeric size based on the shape it will be on
    if shape == 'star' or shape == 'triangle':
        font_multiplier = 0.25
    elif shape == 'rectangle':
        font_multiplier = 0.30
    else:
        font_multiplier = 0.40

    # Set font size, select font style from fonts file, set font color
    font_size = int(round(font_multiplier * image.height))
    font = ImageFont.truetype(font_file, font_size)
    font_color = webcolors.hex_to_rgb(alpha_color)
    draw = ImageDraw.Draw(image)

    # Adjust centering of alphanumerics on shapes
    if shape == 'pentagon':
        xCenter = image.width / 2.8
        yCenter = image.height / 4.8
    elif shape == 'semicircle':
        xCenter = image.width / 2.6
        yCenter = image.height / 5
    elif shape == 'rectangle':
        xCenter = image.width / 2.4
        yCenter = image.height / 4
    elif shape == 'trapezoid':
        xCenter = image.width / 2.8
        yCenter = image.height / 4.8
    elif shape == 'star':
        xCenter = image.width / 2.4
        yCenter = image.height / 3.0
    elif shape == 'triangle':
        xCenter = image.width / 2.4
        yCenter = image.height / 2.7
    elif shape == 'quarter-circle':
        xCenter = image.width / 2.6
        yCenter = image.height / 6.5
    elif shape == 'cross':
        xCenter = image.width / 2.6
        yCenter = image.height / 4
    elif shape == 'square':
        xCenter = image.width / 2.8
        yCenter = image.height / 4.0
    elif shape == 'circle':
        xCenter = image.width / 2.7
        yCenter = image.height / 4.5
    else:
        xCenter = image.width / 3
        yCenter = image.height / 4

    # Places the alphanumeric on the image
    draw.text((xCenter, yCenter), alpha, font_color, font=font)
    return image


def _rotate_shape(image, shape, size, angle, crop):
    border = 100

    if shape in ('rectangle', 'semicircle', 'trapezoid'):
        border *= 2
        crop = crop * 2 + 80

    image = ImageOps.expand(image, border=border, fill='black')
    image = image.rotate(angle)
    image = image.crop((crop, crop, image.width - crop, image.height - crop))
    image = image.resize((size, size), 0)

    # Remove black on corners after rotation.
    image_data = image.getdata()
    new_data = []

    for item in image_data:
        if item[0] < 5 and item[1] < 5 and item[2] < 5:
            new_data.append(0)
        else:
            new_data.append(item)

    image.putdata(new_data)

    return image


def _add_background(image, background, size, padding, blur_radius):
    # Rescaling a copy of the background image, and then pasting the
    # current image on top of it and saving the image as that.
    background_size = size + padding
    background = background.copy().resize((background_size, background_size))

    offset_x = (background.width - image.width) // 2
    offset_y = (background.height - image.height) // 2
    background.paste(image, (offset_x, offset_y), image)

    image = background.filter(ImageFilter.GaussianBlur(blur_radius))

    return image


# Save an image to the output directory.
def _save_image(image, shape, number):
    filename = _format_filename(shape, number)
    image.save(filename)


def _delete_image(shape, number):
    filename = _format_filename(shape, number)
    os.remove(filename)


def _format_filename(shape, number):
    return os.path.join(config.SHAPES_DIR, shape, f'{shape}-{number:06d}.jpg')


if __name__ == '__main__':
    generate_all_shapes()

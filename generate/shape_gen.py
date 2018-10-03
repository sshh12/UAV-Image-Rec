#!/usr/bin/env python3

import glob
import os
import random
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from progress.bar import IncrementalBar
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

    random.setstate(r_state)

    bar = IncrementalBar(f'{shape.title()} Generation', max=config.NUM_SHAPES)

    for i in range(0, config.NUM_SHAPES):
        if i in existing:
            bar.next()
            continue

        image = _create_shape(
            shape, bases[i], backgrounds[i], background_colors[i], alphas[i],
            alpha_colors[i], font_files[i], sizes[i], paddings[i], angles[i],
            crops[i], blur_radii[i]
        )

        _save_image(image, shape, i)

        bar.next()

    bar.finish()


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
    # Start with a sized version of the base shape.
    image = base.copy()
    image.resize((size, size), 0)

    # Apply background color to shape.
    for x in range(image.width):
        for y in range(image.height):
            pixel_color = image.getpixel((x, y))

            if pixel_color[0] == 255 and pixel_color[1] == 255 and \
                    pixel_color[2] == 255:
                image.putpixel((x, y), (255, 255, 255, 0))
            else:
                image.putpixel((x, y), webcolors.hex_to_rgb(background_color))

    # Add on the alphanumeric.
    font_multiplier = 0.4 if shape not in ('star', 'triangle') else 0.3
    font_size = int(round(font_multiplier * image.height))
    font = ImageFont.truetype(font_file, font_size)
    font_color = webcolors.hex_to_rgb(alpha_color)

    draw = ImageDraw.Draw(image)

    draw_x_rel = 1 / 3
    draw_y_rel = 1 / 6 if shape not in ('star', 'triangle') else 1 / 3
    draw_x = image.width * draw_x_rel
    draw_y = image.height * draw_y_rel

    draw.text((draw_x, draw_y), alpha, font_color, font=font)

    # Rotate the image.
    border = 100

    if shape in ('rectangle', 'semicircle', 'trapezoid'):
        border *= 2
        crop = crop * 2 + 80

    image = ImageOps.expand(image, border=border, fill='black')
    image = image.rotate(angle)
    image = image.crop((crop, crop, image.width - crop, image.height - crop))
    image = image.resize((size, size), 0)

    # Make the white parts transparent.
    image = image.convert('RGBA')
    image_data = image.getdata()
    new_data = []

    for item in image_data:
        if item[0] < 5 and item[1] < 5 and item[2] < 5:
            new_data.append(0)
        else:
            new_data.append(item)

    image.putdata(new_data)

    # Rescaling a copy of the background image, and then pasting the
    # current image on top of it and saving the image as that.
    background_size = size + padding
    background = background.copy().resize((background_size, background_size))

    offset_x = (background.width - image.width) // 2
    offset_y = (background.height - image.height) // 2
    background.paste(image, (offset_x, offset_y), image)

    image = background.filter(ImageFilter.GaussianBlur(blur_radius))
    image = image.convert('RGB')

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

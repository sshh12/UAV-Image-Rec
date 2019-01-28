#!/usr/bin/env python3
"""
This script should generate fullsized training images
which contain several artificial shapes.

Save Format:
    data/{train, val}/images/exX.png <- image X
    data/{train, val}/images/exX.txt <- bboxes for image X

BBox Format:
    shape_ALPHA x y width height
    shape2_ALPHA2 x y width height
    ...
"""
import glob
import multiprocessing
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from progress.bar import Bar

import config

# fix me
NUM_GEN = int(config.NUM_IMAGES)
MAX_SHAPES = int(config.MAX_PER_SHAPE)
FULL_SIZE = config.FULL_SIZE
TARGET_COLORS = config.TARGET_COLORS
ALPHA_COLORS = config.ALPHA_COLORS
COLORS = config.COLORS


def generate_all_shapes(gen_type):

    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.DATA_DIR, gen_type, 'images'), exist_ok=True)

    r_state = random.getstate()
    random.seed(gen_type)

    # All the random selection is generated ahead of time, that way
    # the process can be resumed without the shapes changing on each
    # run.

    base_shapes = {}
    for shape in config.SHAPE_TYPES:
        base_shapes[shape] = _get_base_shapes(shape)

    numbers = list(range(0, NUM_GEN))

    backgrounds = _random_list(_get_backgrounds())
    flip_bg = _random_list([False, True])
    mirror_bg = _random_list([False, True])
    blurs = _random_list(range(1, 2))
    num_targets = _random_list(range(1, MAX_SHAPES))

    shape_params = []

    for i in range(NUM_GEN):

        n = num_targets[i]

        shape_names = _random_list(config.SHAPE_TYPES, n)
        bases = [ random.choice(base_shapes[shape]) for shape in shape_names ]
        alphas = _random_list(config.ALPHAS, n)
        font_files = _random_list(config.ALPHA_FONTS, n)

        target_colors = _random_list(TARGET_COLORS, n)
        alpha_colors = _random_list(ALPHA_COLORS, n)

        for i, target_color in enumerate(target_colors):
            if alpha_colors[i] == target_color:
                alpha_colors[i] = 'white'

        target_rgbs = [ random.choice(COLORS[color]) for color in target_colors ]
        alpha_rgbs = [ random.choice(COLORS[color]) for color in alpha_colors ]

        sizes = _random_list(range(35, 55), n)

        angles = _random_list(range(0, 360), n)

        xs = _random_list(range(200, FULL_SIZE[0] - 200, 50), n)
        ys = _random_list(range(200, FULL_SIZE[1] - 200, 50), n)

        shape_params.append(list(zip(shape_names, bases, alphas,
                                font_files, sizes, angles,
                                target_colors, target_rgbs,
                                alpha_colors, alpha_rgbs,
                                xs, ys)))

    # Put everything into one large iterable so that we can split up
    # data across thread pools.
    data = zip(numbers, backgrounds, flip_bg, mirror_bg, blurs, shape_params, [gen_type] * NUM_GEN)

    random.setstate(r_state)

    num_width = str(len(str(NUM_GEN)))
    bar_suffix = '%(index)' + num_width + 'd/%(max)d [%(elapsed_td)s]'

    bar = Bar('Data Generation for ' + gen_type,
              max=NUM_GEN, suffix=bar_suffix)

    # Generate in a pool. If specificed, use a given number of
    # threads.
    with multiprocessing.Pool(None) as pool:
        for i in pool.imap_unordered(_generate_single_example, data):
            bar.next()

    bar.finish()


# One iteration in the function above, runs in a pool.
def _generate_single_example(data):

    number, background, flip_bg, mirror_bg, blur, shape_params, gen_type = data

    background = background.copy()
    if flip_bg:
        background = ImageOps.flip(background)
    if mirror_bg:
        background = ImageOps.mirror(background)

    shape_imgs = [_create_shape(*shape_param) for shape_param in shape_params]

    shape_bboxes, full_img = _add_shapes(background, shape_imgs, shape_params, blur)

    img_fn = os.path.join(config.DATA_DIR, gen_type, 'images', 'ex{}.png'.format(number))
    labels_fn = os.path.join(config.DATA_DIR, gen_type, 'images', 'ex{}.txt'.format(number))

    full_img.save(img_fn)

    with open(labels_fn, 'w') as label_file:
        for shape_bbox in shape_bboxes:
            label_file.write('{} {} {} {} {}\n'.format(*shape_bbox))


def _add_shapes(background, shape_imgs, shape_params, blur_radius):

    shape_bboxes = []

    for i, shape_param in enumerate(shape_params):

        x = shape_param[-2]
        y = shape_param[-1]
        shape_img = shape_imgs[i]

        x1, y1, x2, y2 = shape_img.getbbox()
        bg_at_shape = background.crop((x1 + x, y1 + y, x2 + x, y2 + y))
        bg_at_shape.paste(shape_img, (0, 0), shape_img)
        bg_at_shape = bg_at_shape.filter(ImageFilter.GaussianBlur(blur_radius))

        shape_bboxes.append(("_".join([shape_param[0], shape_param[2]]), x, y, x2 - x1, y2 - y1))

        background.paste(bg_at_shape, (x, y))

    return shape_bboxes, background.convert('RGB')


# Get the background assets. This is returned as list of images.
def _get_backgrounds():

    filenames = glob.glob(os.path.join(config.BACKGROUNDS_DIR, '*.png'))
    filenames += glob.glob(os.path.join(config.BACKGROUNDS_DIR, '*.jpg'))

    return [Image.open(filename).resize(FULL_SIZE) for filename in sorted(filenames)]


# Get the base shape assets. This is returned as list of images.
def _get_base_shapes(shape):
    # filenames = glob.glob(os.path.join(config.BASE_SHAPES_DIR, shape, '*.png'))
    #
    # return [Image.open(sorted(filenames)[0])]
    return [Image.open(os.path.join(config.BASE_SHAPES_DIR, shape, '{}-01.png'.format(shape)))]


# Return a list with items randomly chosen.
def _random_list(items, count=NUM_GEN):
    return [random.choice(items) for i in range(0, count)]


# Create a shape given all the input parameters.
def _create_shape(shape, base, alpha,
                  font_file, size, angle,
                  target_color, target_rgb,
                  alpha_color, alpha_rgb, x, y):

    target_rgb = _augment_color(target_rgb)
    alpha_rgb = _augment_color(alpha_rgb)

    image = _get_base(base, target_rgb, size)
    image = _strip_image(image)
    image = _add_alphanumeric(image, shape, alpha, alpha_rgb, font_file)

    image = image.resize((size, size))
    image = _rotate_shape(image, shape, angle)
    image = _strip_image(image)

    return image


def _augment_color(color_rgb):
    r, g, b = color_rgb
    r = max(min(r + random.randint(-10, 11), 255), 1)
    g = max(min(g + random.randint(-10, 11), 255), 1)
    b = max(min(b + random.randint(-10, 11), 255), 1)
    return (r, g, b)


def _get_base(base, target_rgb, size):
    # Start with a sized version of the base shape.

    image = base.copy()
    image = image.resize((256, 256), 0)
    image = image.convert('RGBA')

    for x in range(image.width):
        for y in range(image.height):

            pixel_color = image.getpixel((x, y))

            if pixel_color[0] != 255 or pixel_color[1] != 255 or pixel_color[2] != 255:
                image.putpixel((x, y), (*target_rgb, 255))

    return image

# remove white and black edges
def _strip_image(image):

    for x in range(image.width):
        for y in range(image.height):

            pixel_color = image.getpixel((x, y))

            if pixel_color[0] == 255 and pixel_color[1] == 255 and pixel_color[2] == 255:
                image.putpixel((x, y), (0, 0, 0, 0))

    image = image.crop(image.getbbox())

    return image


def _add_alphanumeric(image, shape, alpha, alpha_rgb, font_file):
    # Adjust alphanumeric size based on the shape it will be on
    if shape == 'star':
        font_multiplier = 0.14
    if shape == 'triangle':
        font_multiplier = 0.5
    elif shape == 'rectangle':
        font_multiplier = 0.72
    elif shape == 'quarter-circle':
        font_multiplier = 0.60
    elif shape == 'semicircle':
        font_multiplier = 0.55
    elif shape == 'circle':
        font_multiplier = 0.55
    elif shape == 'square':
        font_multiplier = 0.60
    elif shape == 'trapezoid':
        font_multiplier = 0.60
    else:
        font_multiplier = 0.55

    # Set font size, select font style from fonts file, set font color
    font_size = int(round(font_multiplier * image.height))
    font = ImageFont.truetype(font_file, font_size)
    draw = ImageDraw.Draw(image)

    w, h = draw.textsize(alpha, font=font)

    x = (image.width - w) / 2
    y = (image.height - h) / 2

    # Adjust centering of alphanumerics on shapes
    if shape == 'pentagon':
        pass
    elif shape == 'semicircle':
        pass
    elif shape == 'rectangle':
        pass
    elif shape == 'trapezoid':
        y -= 20
    elif shape == 'star':
        pass
    elif shape == 'triangle':
        y += 50
        x -= 120
    elif shape == 'quarter-circle':
        y -= 40
        x += 14
    elif shape == 'cross':
        y -= 25
    elif shape == 'square':
        y -= 10
    elif shape == 'circle':
        pass
    else:
        pass

    draw.text( (x, y) , alpha, alpha_rgb, font=font)

    return image


def _rotate_shape(image, shape, angle):

    image = image.rotate(angle, expand=1)

    return image


if __name__ == '__main__':
    generate_all_shapes('train')
    generate_all_shapes('val')

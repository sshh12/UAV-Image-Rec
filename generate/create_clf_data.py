#!/usr/bin/env python3

from tqdm import tqdm
from PIL import Image
import random
import config
import glob
import os


# Get constants from config
CLF_WIDTH, CLF_HEIGHT = config.PRECLF_SIZE
CROP_WIDTH, CROP_HEIGHT = config.CROP_SIZE
OVERLAP = config.CROP_OVERLAP
RATIO = CLF_WIDTH / CROP_WIDTH
FILE_PATH = os.path.abspath(os.path.dirname(__file__))
CLASSES = config.CLF_TYPES


def contains_shape(x1, y1, x2, y2, data):
    """Check if their is a bbox within these coords"""
    for shape_desc, bx, by, bw, bh in data:

        if x1 < bx < bx + bw < x2 and y1 < by < by + bh < y2:
            return True

    return False


def create_clf_data(dataset_name, dataset_path, image_name, image, data):
    """Generate data for the classifier model"""
    full_width, full_height = image.size

    backgrounds = []
    shapes = []

    for y1 in range(0, full_height - CROP_HEIGHT, CROP_HEIGHT - OVERLAP):

        for x1 in range(0, full_width - CROP_WIDTH, CROP_WIDTH - OVERLAP):

            y2 = y1 + CROP_HEIGHT
            x2 = x1 + CROP_WIDTH

            cropped_img = image.crop((x1, y1, x2, y2))
            cropped_img = cropped_img.resize((CLF_WIDTH, CLF_HEIGHT))

            if contains_shape(x1, y1, x2, y2, data):
                shapes.append(cropped_img)
            else:
                backgrounds.append(cropped_img)

    # Keep classes balanced and randomize data
    num_data = min(len(backgrounds), len(shapes))
    random.shuffle(backgrounds)
    random.shuffle(shapes)

    list_fn = os.path.join(dataset_path,
                           '{}_list.txt'.format(dataset_name))

    for i in range(num_data):

        shape_fn = '{}_{}_{}.png'.format(CLASSES[1], image_name, i)
        shape_path = os.path.join(FILE_PATH, dataset_path, shape_fn)

        bg_fn = '{}_{}_{}.png'.format(CLASSES[0], image_name, i)
        bg_path = os.path.join(FILE_PATH, dataset_path, bg_fn)

        shapes[i].save(shape_path)
        backgrounds[i].save(bg_path)

        with open(list_fn, 'a') as list_file:
            list_file.write(shape_path + "\n")
            list_file.write(bg_path + "\n")


def convert_data(dataset_type, num, offset=0):

    new_dataset = 'clf_' + dataset_type
    images_path = os.path.join(config.DATA_DIR, dataset_type, 'images')
    new_images_path = os.path.join(config.DATA_DIR, new_dataset, 'images')

    os.makedirs(new_images_path, exist_ok=True)

    if offset == 0:
        new_list_fn = '{}_list.txt'.format(new_dataset)
        with open(os.path.join(new_images_path, new_list_fn), 'w') as im_list:
            im_list.write("")

    dataset_images = [os.path.join(images_path, f'ex{i}.png')
                      for i in range(offset, num + offset)]

    for img_fn in tqdm(dataset_images):

        label_fn = img_fn.replace('.png', '.txt')

        image_data = []

        with open(label_fn, 'r') as label_file:
            for line in label_file.readlines():
                shape_desc, x, y, w, h = line.strip().split(' ')
                x, y, w, h = int(x), int(y), int(w), int(h)
                image_data.append((shape_desc, x, y, w, h))

        image_name = os.path.basename(img_fn).replace('.png', '')

        create_clf_data(new_dataset,
                        new_images_path,
                        image_name,
                        Image.open(img_fn),
                        image_data)

        if config.DELETE_ON_CONVERT:
            os.remove(img_fn)
            os.remove(label_fn)


if __name__ == "__main__":
    convert_data('train', config.NUM_IMAGES, config.NUM_OFFSET)
    convert_data('val', config.NUM_VAL_IMAGES, config.NUM_VAL_OFFSET)

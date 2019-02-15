#!/usr/bin/env python3

from tqdm import tqdm
from PIL import Image
import config
import glob
import os


# Get constants from config
DET_WIDTH, DET_HEIGHT = config.DETECTOR_SIZE
CROP_WIDTH, CROP_HEIGHT = config.CROP_SIZE
OVERLAP = config.CROP_OVERLAP
RATIO = DET_WIDTH / CROP_WIDTH
FILE_PATH = os.path.abspath(os.path.dirname(__file__))
CLASSES = config.SHAPE_TYPES


def get_converted_bboxes(x1, y1, x2, y2, data):
    """Find bboxes in coords and convert them to yolo format"""
    bboxes = []

    for shape_desc, bx, by, bw, bh in data:

        shape_name, alpha = shape_desc.split("_")

        if x1 < bx < bx + bw < x2 and y1 < by < by + bh < y2:

            # Yolo3 Format
            # class_idx center_x/im_w center_y/im_h w/im_w h/im_h
            bboxes.append((CLASSES.index(shape_name),
                          (bx - x1 + bw / 2) * RATIO / DET_WIDTH,
                          (by - y1 + bh / 2) * RATIO / DET_HEIGHT,
                          bw * RATIO / DET_WIDTH,
                          bh * RATIO / DET_HEIGHT))

    return bboxes


def create_detector_data(dataset_name, dataset_path, image_name, image, data):
    """Generate data for the detector model"""
    full_width, full_height = image.size

    k = 0

    for y1 in range(0, full_height - CROP_HEIGHT, CROP_HEIGHT - OVERLAP):

        for x1 in range(0, full_width - CROP_WIDTH, CROP_WIDTH - OVERLAP):

            y2 = y1 + CROP_HEIGHT
            x2 = x1 + CROP_WIDTH

            cropped_bboxes = get_converted_bboxes(x1, y1, x2, y2, data)

            if len(cropped_bboxes) == 0:
                # discard crop b/c no shape
                continue

            k += 1

            cropped_img = image.crop((x1, y1, x2, y2))
            cropped_img = cropped_img.resize((DET_WIDTH, DET_HEIGHT))

            name = '{}_crop{}'.format(image_name, k)
            bbox_fn = os.path.join(dataset_path, name + '.txt')
            image_fn = os.path.join(FILE_PATH, dataset_path, name + '.png')
            list_fn = '{}_list.txt'.format(dataset_name)
            list_path = os.path.join(dataset_path, list_fn)

            cropped_img.save(image_fn)

            with open(bbox_fn, 'w') as label_file:
                for bbox in cropped_bboxes:
                    label_file.write('{} {} {} {} {}\n'.format(*bbox))

            with open(list_path, 'a') as list_file:
                list_file.write(image_fn + "\n")


def convert_data(dataset_type, num, offset=0):

    new_dataset = 'detector_' + dataset_type
    images_path = os.path.join(config.DATA_DIR, dataset_type, 'images')
    new_images_path = os.path.join(config.DATA_DIR, new_dataset, 'images')

    os.makedirs(new_images_path, exist_ok=True)

    # Clear/create data index
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

        create_detector_data(new_dataset,
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

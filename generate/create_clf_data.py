#!/usr/bin/env python3

from PIL import Image
from progress.bar import Bar
import multiprocessing
import random
import glob
import os
import config


NEW_WIDTH, NEW_HEIGHT = config.PRECLF_SIZE
CROP_WIDTH, CROP_HEIGHT = config.CROP_SIZE
OVERLAP = config.CROP_OVERLAP

RATIO = NEW_WIDTH / CROP_WIDTH


def get_resized_bboxes(x1, y1, x2, y2, bboxes):

    rel_bboxes = []

    w = x2 - x1
    h = y2 - y1

    for shape, bx, by, bw, bh in bboxes:

        shape_name, alpha = shape.split("_")

        if x1 < bx < bx + bw < x2 and y1 < by < by + bh < y2:

            rel_bboxes.append((config.SHAPE_TYPES.index(shape_name),
                                   (bx - x1 + bw / 2) * RATIO / NEW_WIDTH,
                                   (by - y1 + bh / 2) * RATIO / NEW_HEIGHT,
                                   bw * RATIO / NEW_WIDTH,
                                   bh * RATIO / NEW_HEIGHT))

    return rel_bboxes


k = 0

def create_cropped_data(gen_type, i, full_img, bboxes):

    global k

    full_width, full_height = full_img.size

    target_images = []
    background_images = []

    for y1 in range(0, full_height - CROP_HEIGHT, CROP_HEIGHT - OVERLAP):

        for x1 in range(0, full_width - CROP_WIDTH, CROP_WIDTH - OVERLAP):

            y2 = y1 + CROP_HEIGHT
            x2 = x1 + CROP_WIDTH

            cropped_bboxes = get_resized_bboxes(x1, y1, x2, y2, bboxes)

            

            cropped_img = full_img.crop((x1, y1, x2, y2))
            cropped_img = cropped_img.resize((NEW_WIDTH, NEW_HEIGHT), Image.BICUBIC)

            

            if len(cropped_bboxes) == 0:
                label = "background"
            else:
                label = "target"

            name = '{}_{}'.format(k, label)

            full_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), config.DATA_DIR, gen_type, 'images', name + '.png')

            if label == "background":
                background_images.append((cropped_img, full_name))
            else:
                target_images.append((cropped_img, full_name))

            k += 1

    
    n = min(len(target_images), len(background_images))

    random.shuffle(background_images)

    for i in range(n):
        target_images[i][0].save(target_images[i][1])
        background_images[i][0].save(background_images[i][1])
        with open(os.path.join(config.DATA_DIR, gen_type, '{}_list.txt'.format(gen_type)), 'a') as list_file:
            list_file.write(target_images[i][1] + "\n")
            list_file.write(background_images[i][1] + "\n")

            


def main(gen_type):

    os.makedirs(os.path.join(config.DATA_DIR, 'clf_' + gen_type, 'images'), exist_ok=True)

    im_fns = glob.glob(os.path.join(config.DATA_DIR, gen_type, 'images', '*.png'))

    bar = Bar('Cropping', max=len(im_fns))

    with open(os.path.join(config.DATA_DIR, 'clf_' + gen_type, '{}_list.txt'.format('clf_' + gen_type)), 'w') as list_file:
        list_file.write("")

    for img_fn in im_fns:

        label_fn = img_fn.replace('.png', '.txt')

        bboxes = []

        with open(label_fn, 'r') as label_file:
            for line in label_file.readlines():
                shape, x, y, w, h = line.strip().split(' ')
                x, y, w, h = int(x), int(y), int(w), int(h)
                bboxes.append((shape, x, y, w, h))

        create_cropped_data('clf_' + gen_type, os.path.basename(img_fn).replace('.png', ''), Image.open(img_fn), bboxes)

        os.remove(img_fn)
        os.remove(label_fn)

        bar.next()

    bar.finish()


if __name__ == "__main__":
    main('train')
    main('val')

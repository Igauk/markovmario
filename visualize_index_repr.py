import os
import re

import cv2
import matplotlib.pyplot as plt
import numpy as np


def visualize(representation, sprite_path, save=False):
    sprites = []
    for filename in sorted(os.listdir(sprite_path), key=lambda x: int(re.split("[_.]", x)[1])):
        sprites.append(cv2.imread(f"{sprite_path}/{filename}"))
    num_blocks_h, num_blocks_w = representation.shape
    bs = 16
    reconstructed_image = np.zeros((num_blocks_h * bs, num_blocks_w * bs, 3), dtype=np.uint8)
    for i in range(num_blocks_h):
        for j in range(num_blocks_w):
            # Find the corresponding sprite for this block
            block = sprites[representation[i, j]]
            reconstructed_image[i*bs:(i+1)*bs, j*bs:(j+1)*bs, :] = block
    aspect_ratio = num_blocks_w / num_blocks_h
    scaling_factor = 5
    fig = plt.figure(figsize=(aspect_ratio * scaling_factor, scaling_factor))
    plt.axis('off')
    plt.imshow(reconstructed_image), plt.show()
    return reconstructed_image




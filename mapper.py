"""
Encoding represents maps as indices into the sprite array for a particular set of maps
"""
import os
import pickle
import re

import cv2
import numpy as np


def _to_sprite_index(grid_image, unique_blocks):
    """
    Converts the grid image to a sprite index representation
    :param grid_image: The grid-split image.
    :param unique_blocks: Unique blocks for this representation
    :return: Encoded sprite index representation
    """
    m, n, block_size, _, channels = grid_image.shape
    indices = []
    for block in grid_image.reshape(-1, block_size, block_size, channels):
        found = False
        min_mse = np.mean(np.square(block - np.zeros_like(block)))
        closest_idx = 0
        for idx, unique_block in enumerate(unique_blocks):
            if np.array_equal(block, unique_block):
                indices.append(idx)
                found = True
                break
            mse = np.mean(np.square(block - unique_block))
            if mse < min_mse:
                closest_idx = idx
                min_mse = mse
        if not found:
            indices.append(closest_idx)  # Use most similar block to replace
    return np.array(indices).reshape(m, n).astype(np.uint8)


if __name__ == '__main__':
    with open("Scraped/preprocessed_smb1.pkl", 'rb') as f:
        smb1 = pickle.load(f)

    with open("Scraped/preprocessed_smb2.pkl", 'rb') as f:
        smb2 = pickle.load(f)

    SMB1_sprites = []
    SMB2_sprites = []
    for filename in sorted(os.listdir("Scraped/SMB1_Sprites"), key=lambda x: int(re.split("[_.]", x)[1])):
        SMB1_sprites.append(cv2.imread(f"Scraped/SMB1_Sprites/{filename}"))
    for filename in sorted(os.listdir("Scraped/SMB2_Sprites"), key=lambda x: int(re.split("[_.]", x)[1])):
        SMB2_sprites.append(cv2.imread(f"Scraped/SMB2_Sprites/{filename}"))

    for entry in smb1:
        img_id, grid_repr = entry
        sprite_index_repr = _to_sprite_index(grid_repr, SMB1_sprites)
        cv2.imwrite(f"Scraped/SMB1_Data/encoded_{img_id}", sprite_index_repr)

    for entry in smb2:
        img_id, grid_repr = entry
        sprite_index_repr = _to_sprite_index(grid_repr, SMB2_sprites)
        cv2.imwrite(f"Scraped/SMB2_Data/encoded_{img_id}", sprite_index_repr)

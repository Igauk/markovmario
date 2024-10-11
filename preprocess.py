"""
Takes scraped images in order to extract the unique blocks from each level, in order to ultimately store them as sprites
"""
import pickle

import cv2
import numpy as np


def _remove_watermark(image):
    watermark = cv2.cvtColor(cv2.imread("Scraped/watermark.png"), cv2.COLOR_BGR2RGB)

    min_val, _, min_location, _ = cv2.minMaxLoc(cv2.matchTemplate(image, watermark, cv2.TM_SQDIFF))
    cleaned = image.copy()
    x, y = min_location
    cleaned[y:y + watermark.shape[0], x:x + watermark.shape[1]] = np.zeros_like(watermark)
    return cleaned


def _grid_split(image, block_size=16):
    """
    Splits an image into block-size granulars, changing the overall resolution to that of the block
    :param image: To split into blocks
    :param block_size: Number of pixels in a BxB chunk
    """
    h, w, _ = image.shape
    split = np.zeros((h // block_size, w // block_size, block_size, block_size, 3), dtype=np.int32)
    for x in range(block_size, w + 1, block_size):
        for y in range(block_size, h + 1, block_size):
            block_index = y // block_size - 1, x // block_size - 1
            split[block_index] = image[y - block_size:y, x - block_size:x, :]
    return split


def _extract_unique_blocks(grid_representations, output_path):
    """
    Extracts the unique blocks across a collection of grid representations of levels
    :param grid_representations: List of images that have been preprocessed
    """
    num_images = len(grid_representations)
    _, _, bs, _, c = grid_representations[0].shape  # w x h x b x b x c

    # Normalize maps to have the same dimensions to create a numpy array
    max_height_blocks = max([grid.shape[0] for grid in grid_representations])
    max_width_blocks = max([grid.shape[1] for grid in grid_representations])
    for i, grid in enumerate(grid_representations):
        grid_representations[i] = np.resize(grid, (max_height_blocks, max_width_blocks, bs, bs, c))
    grid = np.array(grid_representations)

    # Flatten and find unique instances of blocks
    flattened = grid.reshape(-1, bs * bs * c)
    unique_flattened_blocks, counts = np.unique(flattened, return_counts=True, axis=0)
    sorted_indices = np.argsort(-counts)
    sorted_unique_flattened_blocks = unique_flattened_blocks[sorted_indices]
    sorted_counts = counts[sorted_indices]

    # Keep only instances that appear at least once in every level
    sorted_unique_flattened_blocks = sorted_unique_flattened_blocks[sorted_counts >= num_images]
    unique_blocks = sorted_unique_flattened_blocks.reshape(-1, bs, bs, c)

    # Write those to a file
    for i, block in enumerate(unique_blocks):
        cv2.imwrite(f"{output_path}/sprite_{i}.png", block)


def _preprocess_images(map_images):
    """
    Preprocesses images to return a grid representation without a watermark
    """
    grid = []
    for i, entry in enumerate(map_images):
        img_id, image = entry
        cleaned = _remove_watermark(image)
        grid.append((img_id, np.array(_grid_split(cleaned))))
    return grid


if __name__ == '__main__':
    with open("Scraped/smb1.pkl", 'rb') as f:
        smb1 = pickle.load(f)

    with open("Scraped/smb2.pkl", 'rb') as f:
        smb2 = pickle.load(f)

    smb1_grid = _preprocess_images(smb1)
    smb2_grid = _preprocess_images(smb2)

    # Store preprocessed images for future use
    with open("Scraped/preprocessed_smb1.pkl", 'wb') as f:
        pickle.dump(smb1_grid, f)

    with open("Scraped/preprocessed_smb2.pkl", 'wb') as f:
        pickle.dump(smb2_grid, f)

    # Store the unique blocks for each set of maps
    _extract_unique_blocks([entry[1] for entry in smb1_grid], "Scraped/SMB1_Sprites")
    _extract_unique_blocks([entry[1] for entry in smb2_grid], "Scraped/SMB2_Sprites")

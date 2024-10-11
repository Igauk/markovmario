"""
This script uses the Markov chain saved as a Python dictionary of dictionaries to generate a new level in the sprite
index representation, based on `generate.py`
"""

import pickle
import random

import numpy as np

import visualize_index_repr

# Load up the probability dictionary
markovProbabilities = pickle.load(open("smb1probabilities.pickle", "rb"))

# Parameters determining the size of the level
height = 15  # will end up generating a level with one height larger than this
width = 100
level = np.zeros((height+1, width), dtype=np.uint8)

most_common_sprite = 0
markovCounts = {}  # Dictionary of (x-1, y), (x-1, y+1), (x, y+1)
for y in range(height, -1, -1):
    for x in range(0, width):
        west = level[y, x - 1] if x > 0 else None
        south = level[y + 1, x - 1] if y < height else None
        southwest = level[y + 1, x] if x > 0 and y < height else None
        state = (west, southwest, south)

        # Query the Markov chain to see what tile value we should place at this tile location
        if state in markovProbabilities.keys():
            # Weighted Sampling
            randValue = random.random()
            currProb = 0
            sprite_index = most_common_sprite
            for action in markovProbabilities[state]:
                currProb += markovProbabilities[state][action]
                if currProb > randValue:
                    sprite_index = action
                    break
            level[y, x] = sprite_index
        else:
            level[y, x] = most_common_sprite

visualize_index_repr.visualize(level, "Scraped/SMB1_Sprites")

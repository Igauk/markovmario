"""
This script uses the sprite index representation to train a markov chain based directly on `train.py`
"""

import glob
import os
import pickle

import cv2
import matplotlib.pyplot as plt

import visualize_index_repr

smb1 = []
smb1_path = "Scraped/SMB1_Data"
for file in os.listdir(smb1_path):
    smb1.append(cv2.cvtColor(cv2.imread(f"{smb1_path}/{file}"), cv2.COLOR_BGR2GRAY))

smb2 = []
smb2_path = "Scraped/SMB2_Data"
for file in os.listdir(smb2_path):
    smb2.append(cv2.cvtColor(cv2.imread(f"{smb2_path}/{file}"), cv2.COLOR_BGR2GRAY))


def train_markovmario(levels, outputFile):
    # Extract Markov chain Counts from the levels
    markovCounts = {}  # Dictionary of (x-1, y), (x-1, y+1), (x, y+1)
    for level in levels:  # Looking at one level at a time
        height, width = level.shape[0] - 1, level.shape[1] - 1
        for y in range(height, -1, -1):
            for x in range(0, width):
                west = level[y, x - 1] if x > 0 else None
                south = level[y + 1, x - 1] if y < height else None
                southwest = level[y + 1, x] if x > 0 and y < height else None
                key = (west, southwest, south)

                if key not in markovCounts.keys():
                    markovCounts[key] = {}
                if not level[y, x] in markovCounts[key].keys():
                    markovCounts[key][level[y, x]] = 0

                # Increments the number of times we see the tile value at location (x,y) in this specific level
                markovCounts[key][level[y, x]] += 1.0

    # Normalize markov counts in order to approximate probability values
    markovProbabilities = {}  # The representation of our Markov chain, a dictionary of dictionaries
    for key in markovCounts.keys():
        markovProbabilities[key] = {}

        sumVal = 0
        for key2 in markovCounts[key].keys():
            sumVal += markovCounts[key][key2]
        for key2 in markovCounts[key].keys():
            markovProbabilities[key][key2] = markovCounts[key][key2] / sumVal
    # Save the 'markovProbabilities' dictionary to a file
    pickle.dump(markovProbabilities, open(outputFile, "wb"))


visualize_index_repr.visualize(smb1[10], "Scraped/SMB1_Sprites")
train_markovmario([smb1[8], smb1[10]], "smb1probabilities.pickle")
train_markovmario([smb2[10]], "smb2probabilities.pickle")

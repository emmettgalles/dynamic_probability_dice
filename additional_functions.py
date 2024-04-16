# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:00:28 2022

@author: Emmett Galles
"""
# File that stores functions we call in main.py.
#
#

import random

## === FUNCTIONS ===
# Below merges two lists into a list of tuples. I got this from online
def merge(list1, list2):
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

# Below just rolls a pair of dice with a passed-in probability
def roll_dice(probability):
    # Create the list that will represent different options for dice rolls
    dice = list(range(2, 13))
    # Now roll the dice
    roll = (random.choices(dice, weights=probability, k=1))
    # Return the roll
    return roll
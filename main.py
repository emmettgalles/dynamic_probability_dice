# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 12:44:28 2022

@author: Emmett Galles
"""
## === IMPORTING MODULES ===
import copy, random
from operator import add

## === INITIATING VARIABLES ===
# Create the dice (just a list with possible rolls)
dice = list(range(2, 13))
# We're now going to set the fixed probability of each dice roll (in order, normalized to 1)
fixed_prob = [1/36, 2/36, 3/36, 4/36, 5/36, 6/36, 5/36, 4/36, 3/36, 2/36, 1/36]
# Create the target cumulative distribution (which will end up being the product of number of rolls and stat_dist)
target_dist = [0] * len(dice)
# Create the actual cumulative distribution
actual_dist = copy.copy(target_dist)
# Create the dynamic probability (which is what makes this whole thing different from just a normal dice roll)
dynamic_prob = copy.copy(target_dist)
# Track the rolls
rolls = []

## === FIRST ROLL ===
# Roll the first dice, or in other words, choose a random number from dice with the probability given by fixed_prob
first_roll = (random.choices(dice, weights=fixed_prob, k=1))
# We now increment this in our actual_dist list
actual_dist[first_roll[0]-2] += 1
# Increment the target_dist
target_dist = list(map(add, target_dist, fixed_prob))
# Add the roll to the list of rolls
rolls += first_roll

## === SUBSEQUENT ROLLS ===

# *** can initiate some type of iteration here ***
for i in range(35):
    
    # Increment the target_dist
    target_dist = list(map(add, target_dist, fixed_prob))
    # We adjust the dynamic probability based on what the target_dist is. Note that before we roll, we adjust target_dist because that's what we'll be aiming for when we adjust dynamic_prob. To do that, we subtract actual_dist from target_dist, make any negative values 0, then normalize to whatever the sum of the nonzero values are, and that's the new dynamic_prob
    #
    # Subtract actual_dist from target_dist
    diff_dist = list(map(add, target_dist, [-x for x in actual_dist]))
    # Find negative numbers and set to 0
    #
    # Set counter
    counter = 0
    # Find the negative numbers
    for dist in diff_dist:
        if dist < 0:
            diff_dist[counter] = 0
        counter += 1
    # Now we normalize
    dynamic_prob[:] = [x / sum(diff_dist) for x in diff_dist]
    # And then we can roll
    roll = (random.choices(dice, weights=dynamic_prob, k=1))
    # We now increment this in our actual_dist list
    actual_dist[roll[0]-2] += 1
    # Add it to the list of rolls
    rolls += roll


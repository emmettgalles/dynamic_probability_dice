# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 12:44:28 2022

@author: Emmett Galles
"""
## === IMPORTING MODULES ===
import copy, random
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
from additional_functions import merge, roll_dice

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
# We need to preallocate the adaptive probability
adaptive_prob = []
# Create a rolls and distribution tracker for the theoretical dice
actual_dist_theo = copy.copy(target_dist)
rolls_theo = []

## === ROLLING THE DICE ===
# *** iteration can be done here ***
# Set number of roles here (which will be the number we put in range)
for i in range(80):
    if i == 0:  # First roll
        # Roll the dice, or in other words, choose a random number from dice with the probability given by fixed_prob
        roll = (random.choices(dice, weights=fixed_prob, k=1))
    else:
        # Roll the dice with the adaptive_prob
        roll = (random.choices(dice, weights=adaptive_prob, k=1))
    # We now increment this in our actual_dist list. The subtracion of the roll's value by two is manipulating the value to match up with the correct index (ex: if a six is rolled, six is the 5th item in the list, and since Python indexes starting from zero, the correct index would be 4 = 6 - 2)
    actual_dist[roll[0]-2] += 1
    # Add the roll to the list of rolls
    rolls += roll
    # We need to be a little crafty here. What we're looking to do is figure out what the limiting dice value is. In other words, we want to see how which dice value has had the most improbable occurences, as that is what we'll base our adaptive probability off of. We will find that value, then scale our fixed_prob distribution so that the probability will correspond with how the distribution should look assuming that the limiting dice value can be rolled one more time. For example, imagine that we roll a six, four, and three elevens. Obviously the three elevens is a little lopsided, so what we'll do is scale the fixed_prob distribution so that the probability of rolling an eleven is equal to four (for four rolls). To do this, we'll scale the entire fixed_prob list by 4 / [2 / 36]. Once we have all those numbers after scaling, we'll have to account for the fact of what the past rolls have been by subtracting off those rolls from the distribution. Let's start writing stuff and I'll explain along the way.
    #
    # We need to find the limiting value we do this by piecewise dividing actual_dist by fixed_prob and seeing which index returns the greatest number. In the event of a tie, we need to randomly select which number is chosen.
    scaled_dist = np.divide(actual_dist, fixed_prob)
    # We now find the index (or indices) of the limiting value(s). If we have more than one, we will select one at random.
    limiting_value_index = random.choice([i for i, x in enumerate(scaled_dist) if x == max(scaled_dist)])
    # We now scale fixed_prob by the largest number of scaled_dist. When we do this, we create the statistically accurate distribution that would result in the limiting value's number of rolls occuring. Once this is done, then we need to add another distribution, this other distribution being just fixed_prob to introduce more variability. This allows the probability of the next roll to have a nonzero chance of rolling the limiting value. Think about this extra added fixed_prob as increasing the interia of the adaptivity of the dice, it allows for nonzero probabilities of all rolls while still moving the adaptive probability toward the theoretical distribution.
    #
    # First scale fixed_prob by the largest number of scaled_dist
    scaled_prob = [scaled_dist[limiting_value_index] * a for a in fixed_prob]
    # Now create the additional roll distribution to add on
    # additional_dist = [1 / fixed_prob[limiting_value_index] * b for b in fixed_prob]
    additional_dist = fixed_prob
    # Now sum them together
    scaled_prob_additional = np.add(scaled_prob, additional_dist)
    # We now subtract off previous rolls
    adaptive_scaled_prob_additional = np.subtract(scaled_prob_additional, actual_dist)
    # Now we normalize everything so it's nice to read
    adaptive_prob = [c / sum(adaptive_scaled_prob_additional) for c in adaptive_scaled_prob_additional]
    
    ## === ROLLING BASIC DICE ===
    # We're also going to roll basic dice so we can compare distributions. To do this, we will use our function in additional_functions
    #
    # Roll the dice
    roll_theo = roll_dice(fixed_prob)
    # Now put the result in the theoretical variables
    rolls_theo += roll_theo
    actual_dist_theo[roll_theo[0]-2] += 1
    
    # ## === TRACKING ADAPTIVITY WITH PLOTS ===
    # # Let's try to visualize what's going on. We're gonna plot the fixed probability as a bar chart, then next to it we'll have the actual distribution, then next to THAT we'll have the adaptive probability
    # #
    # # Create normalized actual_dist
    # actual_dist_normal = [d / sum(actual_dist) for d in actual_dist]
    # # What we're first going to do is figure out which values of the normalized actual_dist are greater or lower than the values of fixed_prob. We will merge these two lists into a list of tuples
    # actual_dist_merge = merge(fixed_prob, actual_dist_normal)
    # # Now make a list of green and red, green meaning that actual_dist_normal > fixed_prob and red for the converse
    # colors_actual_dist = ['green' if a < b else 'red' for (a,b) in actual_dist_merge]
    # # We'll do the same merging and comparison analysis for the adaptive probability
    # adaptive_prob_merge = merge(fixed_prob, adaptive_prob)
    # colors_adaptive_prob = ['green' if a < b else 'red' for (a,b) in adaptive_prob_merge]
    # # Pop out the plot
    # get_ipython().run_line_magic('matplotlib', 'qt')
    # # Plot the fixed probability
    # plt.subplot(1, 3, 1)
    # plt.bar(dice, fixed_prob)
    # plt.xticks(dice)
    # # Now the actual distribution
    # plt.subplot(1, 3, 2)
    # plt.bar(dice, actual_dist_normal, color = colors_actual_dist)
    # plt.xticks(dice)
    # # Now the adaptive probability
    # plt.subplot(1, 3, 3)
    # plt.bar(dice, adaptive_prob, color = colors_adaptive_prob)
    # plt.xticks(dice)

## === COMPARING ADAPTIVE DICE WITH FIXED DICE ===
# We will now plot our results comparing the theoretical distribution with the adaptive dice as well as fixed probability dice
# Create normalized actual_dist
actual_dist_normal = [d / sum(actual_dist) for d in actual_dist]
# Create normalized actual_dist_theo
actual_dist_theo_normal = [d / sum(actual_dist_theo) for d in actual_dist_theo]
# Pop out the plot
get_ipython().run_line_magic('matplotlib', 'qt')
# Plot the theoretical distribution
plt.subplot(1, 3, 1)
plt.bar(dice, fixed_prob)
plt.title("Theoretical Distribution")
plt.xticks(dice)
# Now the adaptive probability distribution
plt.subplot(1, 3, 2)
plt.bar(dice, actual_dist_normal)
plt.title("Adaptive Probability Distribution")
plt.xticks(dice)
# Now the fixed probability distribution
plt.subplot(1, 3, 3)
plt.bar(dice, actual_dist_theo_normal)
plt.title("Fixed Probability Distribution")
plt.xticks(dice)





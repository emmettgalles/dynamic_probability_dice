# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 12:44:28 2022

@author: Emmett Galles
"""
## === IMPORTING MODULES ===
import copy, random
import numpy as np
import matplotlib.pyplot as plt
# from IPython import get_ipython
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
# Set up how many rolls we want
num_rolls = 80

## === ROLLING THE DICE ===
# *** iteration can be done here ***
# Set number of roles here (which will be the number we put in range)
for i in range(num_rolls):
    if i == 0:  # First roll
        # Roll the dice, or in other words, choose a random number from dice with the probability given by fixed_prob
        roll = (random.choices(dice, weights=fixed_prob, k=1))
    else:
        # Roll the dice with the adaptive_prob
        roll = (random.choices(dice, weights=adaptive_prob, k=1))
    # We now increment this in our actual_dist list. The subtracion of the roll's value by two is manipulating the value to match up with the correct index (ex: if a six is rolled, six is the 5th item in the list (since the first item is two and the last is twelve), and since Python indexes starting from zero, the correct index would be 4 = 6 - 2)
    #
    # Recall that the variable roll is technically a list (a list with only one element), so roll[0] is getting the value of what we rolled
    actual_dist[roll[0]-2] += 1
    # Add the roll to the list of rolls, which just keeps track of what has been rolled
    rolls += roll
    # We need to be a little crafty here. What we're looking to do is figure out what the limiting dice value is. In other words, we want to see how which dice value has had the most improbable occurences, as that is what we'll base our adaptive probability off of. We will find that value, then scale our fixed_prob distribution so that the probability will correspond with how the distribution should look. Let's start writing stuff and I'll explain along the way.
    #
    # We need to find the limiting value, and we do this by piecewise dividing actual_dist by fixed_prob and seeing which index returns the greatest number. In the event of a tie, we need to randomly select which number is chosen.
    scaled_dist = np.divide(actual_dist, fixed_prob)
    # We now find the index (or indices) of the limiting value(s). If we have more than one, we will select one at random.
    #
    # The list comprehension is a little tricky. The enumerate function takes the list we pass it (in this case, we pass it scaled_dist) and adds the index of each element as a key. For example, if we say ex = enumerate([5,9,2]), then list(ex) = [(0, 5), (1, 9), (2, 2)]. Within the list comprehension, we designate i, x as each tuple in the enumerate object. Using the same example as before, (i_1, x_1) = (0, 5), (i_2, x_2) = (1, 9), and so on. However, our conditional statement of if x == max(scaled_dist) means that we will only take (i, x) tuples such that x = max(scaled_dist). Lastly, notice how we say i for i, x in ..., meaning that we only care about the i values of our tuples, i.e. the indices. Hopefully that clears up all the list comprehension junk.
    limiting_value_index = random.choice([i for i, x in enumerate(scaled_dist) if x == max(scaled_dist)])
    # We now scale fixed_prob by the largest number of scaled_dist. When we do this, we create a theoretically statistical accurate distribution that would result in the limiting value's number of rolls occuring. Once this is done, we then need to add another distribution, this other distribution being just fixed_prob to introduce more variability. This allows the probability of the next roll to have a nonzero chance of rolling the limiting value. Think about this extra added fixed_prob as increasing the interia of the adaptivity of the dice, it allows for nonzero probabilities of all rolls while still moving the adaptive probability toward the theoretical distribution.
    #
    # First scale fixed_prob by the largest number of scaled_dist. Note that scaled_dist[limiting_value_index] * fixed_prob[limiting_value_index] = actual_dist[limiting_value_index]. All other values in scaled_prob will be greater than or equal to actual_dist[limiting_value_index] by design.
    scaled_prob = [scaled_dist[limiting_value_index] * a for a in fixed_prob]
    # Now create the additional roll distribution to add on
    # additional_dist = [1 / fixed_prob[limiting_value_index] * b for b in fixed_prob]
    additional_dist = fixed_prob
    # Now sum them together
    scaled_prob_additional = np.add(scaled_prob, additional_dist)
    # We now subtract off previous rolls. Otherwise, we'd just have a big normal distribution. Subtracting off the previous rolls is what makes the next rolls statistically dependent on the previous rolls.
    #
    # This is a huge part of the script so let's explain it some more. Suppose on our first roll, we roll a 12. After all of our scaling, we have scaled_dist[limiting_value_index] = 36 (since a 12 was rolled). When we multiply each element of fixed_prob by 36, each element now represents how many times we'd have to roll each element in order for our most improbable occurrence (in this case, it's just our single roll of 12 so far) to fit in a normal distribution. This means that we'd need to roll one 2 (1/36 * 36), two 3s (2/36 * 36), etc. To account for what has already been rolled, we subtract away those rolls. In this case, we'd subtract away the single roll of 12 (since we only rolled the dice one time). In other words, after we subtract the previous rolls, we are looking at what is left to be rolled in order to create a normal distribution based on the most improbable occurrence. However, by construction of the scaled_prob, we would have a 0% chance of rolling the value that established the most improbable occurrence (in this case, a 12). This is why we choose to add fixed_prob to scaled_prob, to allow for a non-zero chance of rolling the improbable occurrence value. Another way to think about is that we need all the rolls that scaled_prob presents us, and adding in fixed_prob says that in addition to all those rolls, we're gonna roll the dice again and magically come up with fractional values for each dice value. Once all the scaled_prob rolls are rolled, what would be the best roll to maintain a normal distribution? It would be the magical roll that's equal to fixed_prob. By adding it in before all rolls of scaled_prob are rolled, it creates additional inertia so that our adaptive probability isn't completely lopsided and hell-bent on establishing a normal distribution to the point where it becomes too predictable.
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
# # Pop out the plot
# get_ipython().run_line_magic('matplotlib', 'qt')
# Plot the theoretical distribution
plt.subplot(1, 3, 1)
ax1 = plt.gca()
plt.bar(dice, fixed_prob)
plt.title("Theoretical Distribution")
plt.xticks(dice)
ax1.set_ylim([0, 0.18])
# Now the adaptive probability distribution
plt.subplot(1, 3, 2)
ax2 = plt.gca()
plt.bar(dice, actual_dist_normal)
plt.title("Adaptive Probability Distribution")
plt.xticks(dice)
ax2.set_ylim([0, 0.18])
# Now the fixed probability distribution
plt.subplot(1, 3, 3)
ax3 = plt.gca()
plt.bar(dice, actual_dist_theo_normal)
plt.title("Fixed Probability Distribution")
plt.xticks(dice)
ax3.set_ylim([0, 0.18])
# Show the plot
plt.show()





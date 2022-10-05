# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:00:28 2022

@author: Emmett Galles
"""
# This will be a file that stores functions we call in main.py.
#
#

## === FUNCTIONS ===
# Below merges two lists into a list of tuples. I got this from online
def merge(list1, list2):
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list
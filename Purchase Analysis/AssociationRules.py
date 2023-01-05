# DEVELOPED BY Aleksandra Petkova 24/02/2020

# TODO: Reduce the number of subsets to calculate frequency for by calculating support (test different numbers 10%, 30%)
# The number would vary based on dataset.
# TODO: Calculate confidence
# TODO: Lookup Association Rules for more informaton.

#######################################################################################################################
#                                                                                                                     #

#                                                                                                                     #
#######################################################################################################################

from itertools import combinations


# region UTILITY FUNCTIONS
# Check if a given subset exists in a set.
# @param set - a list representing a set.
# @param subset - a list representing the subset of interest.
#
# @return True if the subset does exist in the given set, False if it does not.
def check_subset_existance(subset, set_):
    all_el_in_set = True

    for element in subset:
        if element not in set_:
            all_el_in_set = False
            break

    return all_el_in_set


# Counts how many times the given subset was seen in the set. (Calls the << check_subset_existance >> function.)
# @param ds - dataset in row format.
# @param subset - a list representing the subset of interest.
#
# @return (int) The frequency of the given subset.
def calc_subset_frequency(ds, subset):
    subset_freq = 0

    for row in ds:

        if check_subset_existance(list(subset), row):
            subset_freq += 1

    return subset_freq
# endregion


# Applies a union on 2 sets.
# @param set_a - "set" of elements.
# @param set_b - "set" of elements.
#
# @return a set that represents the union of the given sets.
def union(set_x, set_y):
    return set_x.union(set_y)


# How often a rule has been found to be true, or how confident we are about this rule.
# Example: conf({bread, butter} => {milk}) = supp({bread, butter} union {milk})/supp({bread, butter})
def calc_confidence(set_union_supp, set_x_supp):
    return set_union_supp/set_x_supp

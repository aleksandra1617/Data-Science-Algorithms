"""
Confidence & Association rules
Number of elements per subset is K and K is limited by the number of unique elements.
"""

# TODO:
#######################################################################################################################
#                                                                                                                     #

#                                                                                                                     #
#######################################################################################################################


import os
from itertools import combinations

import AssociationRules

# CONSTANT VARIABLES
SUPPORT = 0.02   # Issue, the same 2 subsets repeat multiple times, why?


def find_max_subset_el(ds):
    # Sort the rows of the dataset by length
    sorted_ds = sorted(ds, reverse=True, key=len)
    # print(sorted_ds)

    return len(sorted_ds[0])

# Test function
# print(find_max_subset_el([[0,1,2], [0], [0,1,2,3,4,5], [0,1,2,3]]))


# Use Association Rules to filter the subset list so that low frequency items are not flooding the data structure.
# Returns a list of all the possible combinations of the given list of items.
def find_subsets(s, num_elements, ds):
    """
    << find_subsets >> function
    Summary: Finds all the frequent subsets in the given dataset by filtering them out through the use of association rules.

    Performance Improvements:
    The K value, i.e. num_elements is directly responsible about the performance of the algorithm.
    The higher the value the bigger the scope of the search. For example if the largest set has 4 elements,
    searching for subsets of size 5 is redundant and wasteful. From this we can extract the rule that the number
    of elements should never be higher than the size of the largest set in the given dataset.

    Parameters:
    s (string SET): set of all unique items.
    num_elements (int): The K value or max number of elements in each subset.
    ds (2D string list): Row data of customer groceries recites.

    Returns:
    # 3D string LIST: Contains the filtered/frequent combination of the given dataset with their frequencies.
    3D DICTIONARY: Contains the filtered/frequent combination of the given dataset with their frequencies.

    """
    all_subsets = []    # TODO: Convert this to dictionary
    acc_subsets = []

    for num_el_per_subset in range(1, num_elements+1):  # While len(s) != 0
        possible_combinations = list(combinations(s, num_el_per_subset))
        # print("PROCESSING COMBINATIONS WITH K = ", num_el_per_subset)
        # Filter the current combination of subsets using association rules.
        for current_subset in possible_combinations:
            # print("Processing")
            # Subset frequency or Absolute Support
            subset_freq = AssociationRules.calc_subset_frequency(ds, list(current_subset))  # ('dsfdf', 'gdggs')

            # 1) Calculate support for the given subset and check if this subset passes.
            # Example: s{Beer, Eggs} = 1/5 = 20%
            # 1.1) Get number of rows in the dataset.
            num_rows = len(ds)

            # The subset's Relative Support or how many of the rows/sets contain this subset.
            subset_relative_sup = subset_freq / num_rows

            if subset_relative_sup > SUPPORT:
                acc_subsets.append([list(current_subset), subset_freq])
        """"""
        # Apriori Shrink
        s = []
        # Remove all the subsets that are not frequent
        for subset_and_freq in acc_subsets:
            subset = subset_and_freq[0]
            for item in subset:
                s.append(item)

        all_subsets += acc_subsets
        acc_subsets.clear()

    return all_subsets


# print(find_subsets.__doc__)

# Loads the dataset and does any formatting to prepare it to be used. (Called in << main >> function)
def setup_data():
    global data_sample, dataset

    # OPEN FILE
    # print("CWD: ", os.getcwd())
    path = os.getcwd() + "Masters\\Data Mining\\Purchase Analysis\\Data\\groceries.csv"
    print("\nDATASET PATH: ", path)

    # READ FILE
    file_object = open(path, "r")
    dataset = [line.strip().split(',') for line in file_object.readlines()]

    # SELECT SAMPLE
    data_sample = dataset[:2]  # subsets that should survive are to do with yogurt(occ: 3) & whole milk(occ: 3)

    # PEEK AT DATASET
    row_count = len(data_sample)

    print("\nFirst << ", row_count, " >> Rows from the Loaded Data Sample: ")
    for itter in range(row_count):
        row = data_sample[itter]
        print(row)


# TODO: Change this so that main accepts a dataset but is otherwise self-contained
def main():
    global SUPPORT, data_sample, dataset

    setup_data()

    # This is a dictionary which will contain a dictionary for each data item with the item name as the key
    # and tags for the item details of interest.
    item_analysis_data = {}  # TODO: Rename to unique_items

    # u_recite_data Format ->  [['citrus fruit', 'semi-finished bread', 'margarine', 'ready soups'],
    #                           ['citrus fruit', 'semi-finished bread']]
    u_recite_data = []
    u_recite_frequency = []

    # Extract information for each recite in the dataset.
    for purchase in data_sample:
        # region UNIQUE RECITE Frequency
        # Find all the unique recites and calculate their frequency
        if purchase not in u_recite_data:
            u_recite_data.append(purchase)
            u_recite_frequency.append(1)
        else:
            recite_index = u_recite_data.index(purchase)
            u_recite_frequency[recite_index] += 1
        # endregion
        # region UNIQUE ITEM Frequency
        for item in purchase:
            # Update the item_analysis_data dictionary to store all unique items
            if item not in item_analysis_data.keys():
                # print("\tNew item found: ", item)
                # print("\t\tAppending << ", item, " >> item to dictionary. ")
                # print("\t\tList of items in dictionary: ", list(item_analysis_data.keys()))

                item_details = {item: {"Frequency": 1}}
                item_analysis_data.update(item_details)

            else:
                # print("No new items found! \n\n Increasing Frequency: ")
                item_analysis_data[item]["Frequency"] += 1
        # endregion

    # region RECITE SUBSET FREQUENCY (IMPROVEMENTS ADDED WITH ASSOCIATION RULES)
    # 1) Find all the unique subsets
    # 1.1) Fetch a list containing all the unique items.
    unique_item_names = item_analysis_data.keys()

    # 1.2) Find all the subsets for the given dataset.
    print(find_max_subset_el(unique_item_names))
    full_subset_list = find_subsets(unique_item_names, 5, data_sample)
    # subsets_freqencies = [0]*len(full_subset_list)  # Generating a list of 0s with the same length as the subset list
    # print("Full Subset List: ", full_subset_list)
    for i in range(len(full_subset_list)):
        print("SUBSET: ", full_subset_list[i][0], "  FREQUENCY: ", full_subset_list[i][1])

    # 1.3) Calculate Confidence.
    # REL SUPP(Set X = {'yogurt'}) = 3/6 = 0.5
    # REL SUPP(Set Y = {'pip fruit'}) = 1/6 = 0.16

    # REL SUPP( Union of Set X & Set Y {'yogurt', 'pip fruit'}) = 1/6 = 0.16
    print("\nThe Confidence that buying << Yogurt >> results in buying << pip fruit >> is << ", AssociationRules.calc_confidence(0.16, 0.5), " >>")

    # endregion

    # region CONSOLE OUTPUT
    """ print("\n\n Dictionary after analysis: ", item_analysis_data, "\n\n\n")
    print("Frequency of unique Recites:")
    for itterator in range(len(u_recite_data)):
        u_recite = u_recite_data[itterator]
        ur_frequency = u_recite_frequency[itterator]

        print("The frequency of recite: ", u_recite, " is << ", ur_frequency, " >>")
    # print("\n For subset: ", pur_subsets[0][0], " the frequency in the dataset is ", pur_subsets[0][1])
    print(pur_subsets)"""
    # endregion



print("\n\n\n######################################## SUBSETS ########################################")
for count in range(1, 5):
    print("\nThe subsets with ", count, "elements for {'a', 'b', 'c', 'd'} are: \n", list(combinations(["a", "b", "c", "d"], count)))

main()


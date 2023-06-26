# This script was originally provided by https://github.com/Chao-Ran-Erwin

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, rankdata


def AMeasure(a, b):
    m = len(a)
    n = len(b)
    count_greater = 0
    count_equal = 0

    for i in range(m):
        for j in range(n):
            if a[i] > b[j]:
                count_greater += 1
            elif a[i] == b[j]:
                count_equal += 1

    a12 = (count_greater / (m * n)) + 0.5 * (count_equal / (m * n))
    return a12

def calculate_a12(a, b):
    combined = np.hstack((a, b))

    m = len(a)
    n = len(b)
    ranks = rankdata(combined)  # Rank the combined sample

    sum_ranks_a = sum(ranks[:m])  # Sum of ranks for elements in 'a'

    a12 = (sum_ranks_a - (m * (m + 1)) / 2) / (m * n)  # Calculate the A12 measure

    return a12

def compare_algorithms(data, base_data, algorithm1, algorithm2):
    coverage_types = ['branches-covered']
    algorithms = ['RVEA', 'MOSARVEA', 'DynaMOSARVEA']
    base_algorithms = ['random', 'NSGAII', 'MOSA', 'DynaMOSA']

    algorithm1_better_count = 0
    algorithm2_better_count = 0
    equal_count = 0
    no_difference_count = 0

    for coverage_type in coverage_types:
        print(f"Coverage Type: {coverage_type}")

        unique_classes = data['include'].unique()
        for class_value in unique_classes:

            # Compare algorithm1 vs algorithm2 for the current class
            if algorithm1 in algorithms:
                algorithm1_data = data[(data['preset'] == algorithm1) & (data['include'] == class_value)][
                    coverage_type].values
            elif algorithm1 in base_algorithms:
                algorithm1_data = base_data[(base_data['preset'] == algorithm1) & (base_data['include'] == class_value)][
                    coverage_type].values
            else:
                raise Exception("Invalid algorithm: ", algorithm1)

            if algorithm2 in algorithms:
                algorithm2_data = data[(data['preset'] == algorithm2) & (data['include'] == class_value)][
                    coverage_type].values
            elif algorithm2 in base_algorithms:
                algorithm2_data = base_data[(base_data['preset'] == algorithm2) & (base_data['include'] == class_value)][
                    coverage_type].values
            else:
                raise Exception("Invalid algorithm: ", algorithm2)

            # Skip the comparison if the difference is zero for all elements
            if (algorithm1_data - algorithm2_data == 0).all():
                no_difference_count += 1
                continue

            statistic, p_value = wilcoxon(algorithm1_data, algorithm2_data)
            a12 = AMeasure(algorithm1_data, algorithm2_data)
            ca = calculate_a12(algorithm1_data, algorithm2_data)

            if p_value <= 0.05:
                print(f"Class: {class_value}")
                print(f"Comparison: {algorithm1} vs {algorithm2}")
                print("Test statistic:", statistic)
                print("P-value:", p_value)
                print("A12:", a12)
                print('other a12', ca)
                print()

                if a12 > 0.5:
                    algorithm1_better_count += 1
                elif a12 < 0.5:
                    algorithm2_better_count += 1
                else:
                    equal_count += 1
            else:
                no_difference_count += 1

    print("Summary:")
    print(f"{algorithm1}  was better {algorithm1_better_count} times.")
    print(f"{algorithm2} was better {algorithm2_better_count} times.")
    print(f"Equal A12 {equal_count} times.")
    print(f"There was no significant difference {no_difference_count} times.")


path_file_data = 'properties.csv'
path_file_data_base = 'properties_base.csv'

# Algorithm data
data = pd.read_csv(path_file_data)

# Base algorithm data
base_data = pd.read_csv(path_file_data_base)

# Compare the algorithms for different coverage types
compare_algorithms(data, base_data, "random", "DynaMOSARVEA")

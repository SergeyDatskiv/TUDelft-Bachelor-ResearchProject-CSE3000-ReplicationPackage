# This script was originally provided by https://github.com/Chao-Ran-Erwin

import pandas as pd
import numpy as np

# Algorithm data
path_file_data = 'properties.csv'
path_file_data_base = 'properties_base.csv'

data = pd.read_csv(path_file_data)
base_data = pd.read_csv(path_file_data_base)
# Create a dictionary to store coverage percentages
coverage_dict = {
    'File Name': [],
    'RVEA': [],
    'MOSARVEA': [],
    'DynaMOSARVEA': [],
    'DynaMOSA': []
}

# Calculate coverage percentage per class per algorithm
coverage_types = ['branches-covered'
    # , 'statements-covered', 'functions-covered'
                  ]
coverage_total = ['branches-total'
    # , 'statements-total', 'functions-total'
                  ]
algorithms = ['RVEA', 'MOSARVEA', 'DynaMOSARVEA']
base_algorithms = ['DynaMOSA']
for coverage_type, total_type in zip(coverage_types, coverage_total):
    # Iterate over unique class values
    unique_classes = data['include'].unique()
    for class_value in unique_classes:
        # Extract file name from class value and remove closing bracket
        file_name = class_value.split('/')[-1][:-1]

        # Filter data for the current class
        class_data = data[data['include'] == class_value]
        base_class_data = base_data[base_data['include'] == class_value]
        # Calculate coverage percentage for each algorithm
        percentages = []
        for algorithm in algorithms:
            algorithm_data = class_data[class_data['preset'] == algorithm]
            total_coverage = algorithm_data[total_type].sum()
            covered_coverage = algorithm_data[coverage_type].sum()
            coverage_percentage = (covered_coverage / total_coverage) * 100
            percentages.append(coverage_percentage)
        for algorithm in base_algorithms:
            algorithm_data = base_class_data[base_class_data['preset'] == algorithm]
            total_coverage = algorithm_data[total_type].sum()
            covered_coverage = algorithm_data[coverage_type].sum()
            coverage_percentage = (covered_coverage / total_coverage)
            percentages.append(coverage_percentage)
        # Add coverage percentages to the dictionary
        coverage_dict['File Name'].append(file_name)
        coverage_dict['RVEA'].append(percentages[0])
        coverage_dict['MOSARVEA'].append(percentages[1])
        coverage_dict['DynaMOSARVEA'].append(percentages[2])
        coverage_dict['DynaMOSA'].append(percentages[3])

# Create a DataFrame from the coverage dictionary
coverage_df = pd.DataFrame(coverage_dict)

# Export the DataFrame as a table in a text file
coverage_df.to_latex('coverage_table.txt')

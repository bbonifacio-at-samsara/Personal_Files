import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os
import seaborn as sns
import re

# Define the CSV file path
csv_file = "Measuring_Bitrate_Error/Data/local/combined.csv"

# Read the CSV file
with open(csv_file, 'r') as file:
    data = file.read()

# Cleaning the data
cleaned_data = re.sub(r'functional_test\.go:974:\s*', '', data)
data_lines = [line.split(', ') for line in cleaned_data.strip().split('\n')]

# Creating the DataFrame
columns = [
    'Expected_Bytes', 'Actual_Bytes', 'Bitrate_Deviation_Percent', 'Duration_of_Experiment', 
    'Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 
    'Codec', 'Stream'
]
df = pd.DataFrame(data_lines, columns=columns)

# Converting appropriate columns to numeric
df['Expected_Bytes'] = pd.to_numeric(df['Expected_Bytes'])
df['Actual_Bytes'] = pd.to_numeric(df['Actual_Bytes'])
df['Bitrate_Deviation_Percent'] = df['Bitrate_Deviation_Percent'].str.rstrip('%').astype(float)
df['Duration_of_Experiment'] = pd.to_numeric(df['Duration_of_Experiment'])
df['Bitrate'] = pd.to_numeric(df['Bitrate'])
df['Framerate'] = pd.to_numeric(df['Framerate'])

# Grouping by the unique categorical combinations and duration
grouped = df.groupby(['Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 'Codec', 'Stream', 'Duration_of_Experiment'])

# Calculate mean and 3 times the standard deviation for each group
summary = grouped['Bitrate_Deviation_Percent'].agg(['mean', 'std']).reset_index()
summary['3x_std'] = summary['std'] * 3

# Plotting
plt.figure(figsize=(12, 8), dpi = 300)
unique_combinations = summary.groupby(['Bitrate', 'Framerate','Resolution', 'Bitrate_Control', 'IDR_Interval', 'Codec', 'Stream'])

for name, group in unique_combinations:
    plt.errorbar(group['Duration_of_Experiment'], group['mean'], yerr=group['3x_std'], fmt='-o', capsize=5, label=f'{name}')

plt.axhline(y=15, color='r', linestyle='--', label='±15 (Maximum allowed Error)')
plt.axhline(y=-15, color='r', linestyle='--')
plt.title('Mean Bitrate Deviation Percent with 3x Standard Deviation over Different Durations for Unique Combinations on Local Machine')
plt.xlabel('Duration of Experiment (seconds)')
plt.ylabel('Mean Bitrate Deviation Percent')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

# Save the plot
storage = "Measuring_Bitrate_Error/Plots/local/Overall/"
if not os.path.exists(storage):
    os.makedirs(storage)
plt.savefig(storage + 'mean_bitrate_deviation_unique_combinations.png', bbox_inches='tight')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os
import seaborn as sns
import re

# Define the CSV file path
csv_file = "Measuring_Bitrate_Error/Data/buildkite/30_second.csv"

# Read the CSV file
with open(csv_file, 'r') as file:
    data = file.read()

# Cleaning the data
cleaned_data = re.sub(r'functional_test\.go:476:\s*', '', data)
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

# Grouping by the unique categorical combinations including bitrate and framerate
grouped = df.groupby(['Resolution', 'Bitrate_Control', 'IDR_Interval', 'Codec', 'Stream', 'Bitrate', 'Framerate'])

# Calculate mean and 3 times the standard deviation for each group
summary = grouped['Bitrate_Deviation_Percent'].agg(['mean', 'std']).reset_index()
summary['3x_std'] = summary['std'] * 3

# Plotting
plt.figure(figsize=(15, 10), dpi=300)
bars = plt.bar(range(len(summary)), summary['mean'], yerr=summary['3x_std'], capsize=5)

# Adding labels to the bars
plt.xticks(range(len(summary)), summary.apply(lambda row: f"{row['Resolution']}, {row['Bitrate_Control']}, {row['IDR_Interval']}, {row['Codec']}, {row['Stream']}, {row['Bitrate']}, {row['Framerate']}", axis=1), rotation=90)

plt.axhline(y=15, color='r', linestyle='--', label='±15')
plt.axhline(y=-15, color='r', linestyle='--')
plt.title('Mean Bitrate Deviation Percent with 3x Standard Deviation for Unique Combinations (30 Seconds) On Buildkite')
plt.xlabel('Unique Combinations')
plt.ylabel('Mean Bitrate Deviation Percent')
plt.legend()
plt.grid(True)

# Save the plot
storage = "Measuring_Bitrate_Error/Plots/buildkite/Overall/"
if not os.path.exists(storage):
    os.makedirs(storage)
plt.savefig(storage + 'histogram_mean_bitrate_deviation_30_seconds.png', bbox_inches='tight')
plt.show()

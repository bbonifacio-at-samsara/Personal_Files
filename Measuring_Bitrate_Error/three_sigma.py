import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os
import seaborn as sns
from tqdm import tqdm
import re

# DataFrame to hold the results
results = []
acceptedError = 15
source = "local/"
# List of seconds to process
seconds_list = ["01", "02", "03", "05", "10", "20", "30"]
seconds_list = [source + i for i in seconds_list]

for seconds in tqdm(seconds_list, desc="Processing Data"):

    # Read the CSV file
    csv_file = "Measuring_Bitrate_Error/Data/" + seconds + "_second.csv"
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

    # Calculate mean and 3 times the standard deviation of Bitrate Deviation Percent
    mean_bitrate_deviation = np.mean(df['Bitrate_Deviation_Percent'])
    std_bitrate_deviation = np.std(df['Bitrate_Deviation_Percent'])
    error_bars = 3 * std_bitrate_deviation
    
    # Append the results
    results.append((int(seconds), mean_bitrate_deviation, error_bars))

# Convert results to DataFrame
results_df = pd.DataFrame(results, columns=['Seconds', 'Mean_Bitrate_Deviation', 'Error_Bars'])

# Sort by Seconds
results_df = results_df.sort_values(by='Seconds')

# Plotting the results
plt.figure(figsize=(10, 6))
plt.errorbar(results_df['Seconds'], results_df['Mean_Bitrate_Deviation'], yerr=results_df['Error_Bars'], fmt='-o', capsize=5)
plt.axhline(y=acceptedError, color='r', linestyle='--')
plt.axhline(y=-acceptedError, color='r', linestyle='--')
plt.title('Mean Bitrate Deviation Percent with 3x Standard Deviation over Different Durations')
plt.xlabel('Duration (seconds)')
plt.ylabel('Mean Bitrate Deviation Percent')
plt.grid(True)

# Save the plot
storage = "Measuring_Bitrate_Error/Plots/Overall/"
if not os.path.exists(storage):
    os.makedirs(storage)
plt.savefig(storage + 'mean_bitrate_deviation_over_time_with_std.png')
plt.show()

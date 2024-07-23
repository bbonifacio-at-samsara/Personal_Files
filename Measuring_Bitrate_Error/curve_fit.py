import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import numpy as np
import os
import seaborn as sns
from tqdm import tqdm
import re

acceptedError = 15
source = "local/"
# List of seconds to process
seconds_list = ["01", "02", "03", "05", "10", "20", "30"]
seconds_list = [source + i for i in seconds_list]

# Define the function to fit
def fit_function(time, a, b):
    return a / np.sqrt(time) + b



# DataFrame to hold the results
results = []

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

    # Calculate mean and SEM of Bitrate Deviation Percent
    mean_bitrate_deviation = np.mean(df['Bitrate_Deviation_Percent'])
    sem_bitrate_deviation = stats.sem(df['Bitrate_Deviation_Percent'])
    
    # Append the results
    results.append((int(seconds), mean_bitrate_deviation, sem_bitrate_deviation))

# Convert results to DataFrame
results_df = pd.DataFrame(results, columns=['Seconds', 'Mean_Bitrate_Deviation', 'SEM_Bitrate_Deviation'])

# Sort by Seconds
results_df = results_df.sort_values(by='Seconds')

# Fit the curve
popt, pcov = curve_fit(fit_function, results_df['Seconds'], results_df['Mean_Bitrate_Deviation'])
a, b = popt
perr = np.sqrt(np.diag(pcov))

# Calculate R²
residuals = results_df['Mean_Bitrate_Deviation'] - fit_function(results_df['Seconds'], *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((results_df['Mean_Bitrate_Deviation'] - np.mean(results_df['Mean_Bitrate_Deviation']))**2)
r_squared = 1 - (ss_res / ss_tot)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.errorbar(results_df['Seconds'], results_df['Mean_Bitrate_Deviation'], yerr=results_df['SEM_Bitrate_Deviation'], fmt='o', capsize=5, label='Data')
plt.plot(results_df['Seconds'], fit_function(results_df['Seconds'], *popt), 'r-', label=f'Fit: a/sqrt(time) + b\na={a:.2f}±{perr[0]:.2f}, b={b:.2f}±{perr[1]:.2f}\nR²={r_squared:.2f}')
plt.title('Mean Bitrate Deviation Percent with 3x Standard Deviation over Different Durations')
plt.xlabel('Duration (seconds)')
plt.ylabel('Mean Bitrate Deviation Percent')
plt.axhline(y=acceptedError, color='r', linestyle='--', label=f'±{acceptedError}')
plt.axhline(y=-acceptedError, color='r', linestyle='--')
plt.legend()
plt.grid(True)

# Save the plot
storage = "Measuring_Bitrate_Error/Plots/Overall/"
if not os.path.exists(storage):
    os.makedirs(storage)
plt.savefig(storage + 'mean_bitrate_deviation_over_time_with_fit.png')
plt.show()

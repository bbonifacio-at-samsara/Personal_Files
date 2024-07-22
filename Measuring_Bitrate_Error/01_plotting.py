import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import numpy as np

# Read the CSV file
csv_file = "Measuring_Bitrate_Error/Data/02_second.csv"
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

# print out the first row for debugging and its labels
print(df.head())
print(df.columns)



# Function to create and save histograms with average, standard deviation, and SEM
def plot_entire_bitrate_deviation(df, storage="Measuring_Bitrate_Error/Plots/02_second/", title=""):
    # Histogram of Bitrate Deviation Percent
    plt.figure(figsize=(10, 6))
    data = df['Bitrate_Deviation_Percent']
    plt.hist(data, bins=10, edgecolor='black')
    plt.title('Histogram of Bitrate Deviation Percent for ' + title)
    plt.xlabel('Bitrate Deviation Percent')
    plt.ylabel('Frequency')
    plt.grid(True)
    
    # Calculate average, standard deviation, and SEM
    avg = np.mean(data)
    std_dev = np.std(data)
    sem = stats.sem(data)
    
    # Add text box for average, standard deviation, and SEM
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (avg, ),
        r'$\sigma=%.2f$' % (std_dev, ),
        r'$SEM=%.2f$' % (sem, )))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=14,
             verticalalignment='top', bbox=props)
    
    plt.savefig(storage + 'histogram_bitrate_deviation_percent.png')

# Creating the histograms
plot_entire_bitrate_deviation(df, title = "02_second")

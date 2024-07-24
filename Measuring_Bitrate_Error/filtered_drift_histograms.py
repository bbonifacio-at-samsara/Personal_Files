import pandas as pd
import os
import matplotlib.pyplot as plt

def read_and_filter_data(directory_list):
    data = pd.DataFrame()
    for directory in directory_list:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.csv'):
                    file_path = os.path.join(dirpath, filename)
                    df = pd.read_csv(file_path)
                    # Filter data for specific resolutions
                    df = df[(df['Resolution'].isin(['RESOLUTION_640X360', 'RESOLUTION_1280X720']))]
                    data = pd.concat([data, df], ignore_index=True)
    return data

def plot_histograms(data, output_path):
    plt.figure(figsize=(10, 6))
    # Filter specific streams and plot their histograms
    for resolution in ['RESOLUTION_640X360', 'RESOLUTION_1280X720']:
        filtered_data = data[data['Resolution'] == resolution]
        plt.hist(filtered_data['Bitrate_Deviation_Percent'], bins=50, alpha=0.5, label=resolution, edgecolor='black')
    
    plt.xlabel('Bitrate Deviation Percent')
    plt.ylabel('Frequency')
    plt.title('Histogram of Bitrate Deviation Percent by Resolution')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.savefig(output_path)  # Save the plot as a file
    plt.show()

# Directory containing CSV files
directory_list = ['path/to/data/directory']

# Read and filter data
filtered_data = read_and_filter_data(directory_list)

# Plot histograms and save the output
output_histogram_path = 'resolution_histogram.png'
plot_histograms(filtered_data, output_histogram_path)

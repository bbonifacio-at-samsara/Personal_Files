import pandas as pd
import os
import matplotlib.pyplot as plt

def read_and_filter_data(directory_list):
    """Read data from the provided directory list and filter based on specified conditions."""
    data = pd.DataFrame()
    for directory in directory_list:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.csv'):
                    file_path = os.path.join(dirpath, filename)
                    df = pd.read_csv(file_path)
                    # Filter data based on the resolution criteria
                    df = df[df['Resolution'].isin(['RESOLUTION_640X360', 'RESOLUTION_1280X720'])]
                    data = pd.concat([data, df], ignore_index=True)
    return data

def plot_histograms(categories_data, output_path):
    """Generate histograms for each category and save the output."""
    plt.figure(figsize=(10, 6))
    for i, data in enumerate(categories_data, 1):
        plt.hist(data['Bitrate_Deviation_Percent'], bins=50, alpha=0.5, label=f'Category {i}', edgecolor='black')
    
    plt.xlabel('Bitrate Deviation Percent')
    plt.ylabel('Frequency')
    plt.title('Histogram of Bitrate Deviation Percent by Category')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.savefig(output_path)  # Save the plot as a file
    plt.show()

# Path to the parent directory containing subdirectories for each category
parent_dir = 'Measuring_Bitrate_Error/Data/nightly_test_processed'

# List of directory lists for each category
categories_directories = [
    [os.path.join(parent_dir, '278018087163919')],
    [os.path.join(parent_dir, '278018087164572')],
    [os.path.join(parent_dir, '278018087164013')],
]

# Read and filter data for each category
categories_data = [read_and_filter_data(category) for category in categories_directories]

# Output histogram path
output_histogram_path = 'Drift of Device Comparison.png'

# Generate and save histograms
plot_histograms(categories_data, output_histogram_path)

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def read_and_filter_data(directory_list):
    """Read and filter data from directories."""
    data = pd.DataFrame()
    for directory in directory_list:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.csv'):
                    file_path = os.path.join(dirpath, filename)
                    df = pd.read_csv(file_path)
                    df = df[df['Resolution'].isin(['RESOLUTION_640X360', 'RESOLUTION_1280X720'])]
                    data = pd.concat([data, df], ignore_index=True)
    return data

def plot_kde(categories_data, categories_labels, output_path):
    """Generate KDE for each category and include variance and its error in the legend."""
    plt.figure(figsize=(10, 6))
    for data, label in zip(categories_data, categories_labels):
        variance = np.var(data['Bitrate_Deviation_Percent'])
        std_dev = np.std(data['Bitrate_Deviation_Percent'])
        label_with_var = f'{label} (Variance: {variance:.2f} ± {std_dev:.2f})'
        data['Bitrate_Deviation_Percent'].plot(kind='kde', linewidth=2, label=label_with_var)
    
    plt.xlabel('Bitrate Deviation Percent')
    plt.ylabel('Normalized Probability Density')
    plt.suptitle('Hardware Reliability Drift on the Nightly Test Devices')
    #plt.title('Distribution of Bitrate Deviation Percent for H26xBitrateFunctionality Test for Resolutions 640x360 and 1280x720 on Nightly Tests in the Past Month')
    # Make the title smaller
    plt.title('Distribution of Bitrate Deviation Percent for the H26xBitrateFunctionality Test \n at Resolutions 640x360 and 1280x720 on Nightly Tests in the Past Month', fontsize=10)
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.savefig(output_path)
    plt.show()

# Specify the parent directory containing subdirectories for each category
parent_dir = 'Measuring_Bitrate_Error/Data/nightly_test_processed'

# Define directory lists and labels for each category
categories_directories = [
    os.path.join(parent_dir, '278018087163919'),
    os.path.join(parent_dir, '278018087164572'),
    os.path.join(parent_dir, '278018087164013'),
]
categories_labels = [
    'Device 278018087163919',
    'Device 278018087164572',
    'Device 278018087164013'
]

# Read and filter data for each category
categories_data = [read_and_filter_data([dir_path]) for dir_path in categories_directories]

# Define the output path for the KDE plot
output_kde_path = 'KDE Device Comparison with Error.png'

# Generate and save KDE plots
plot_kde(categories_data, categories_labels, output_kde_path)

import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy import stats
import numpy as np
import os
import seaborn as sns
from tqdm import tqdm

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

    # Print out the first row for debugging and its labels

    # Function to create and save histograms with average, standard deviation, and SEM
    def plot_entire_bitrate_deviation(df, storage="Measuring_Bitrate_Error/Plots/" + seconds + "_second/", title=""):
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

        # Make the directory if it doesn't exist
        if not os.path.exists(storage):
            os.makedirs(storage)
        
        plt.savefig(storage + 'histogram_bitrate_deviation_percent.png')

    # Creating the histograms
    plot_entire_bitrate_deviation(df, title="" + seconds + "_second")

    # Function to create and save scatter plots for numeric variables
    def create_scatter_plots(df, storage="Measuring_Bitrate_Error/Plots/" + seconds + "_second/"):
        numeric_variables = [
            'Expected_Bytes', 'Actual_Bytes', 'Duration_of_Experiment', 
            'Bitrate', 'Framerate'
        ]
        
        for var in numeric_variables:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=var, y='Bitrate_Deviation_Percent')
            plt.title(f'Correlation between {var} and Bitrate Deviation Percent')
            plt.xlabel(var)
            plt.ylabel('Bitrate Deviation Percent')
            plt.grid(True)
            
            # Make the directory if it doesn't exist
            if not os.path.exists(storage):
                os.makedirs(storage)
            
            plt.savefig(storage + f'scatter_{var.lower()}_bitrate_deviation_percent.png')

    # Function to create and save bar plots for categorical variables
    def create_bar_plots(df, storage="Measuring_Bitrate_Error/Plots/" + seconds + "_second/"):
        categorical_variables = [
            'Resolution', 'Bitrate_Control', 'IDR_Interval', 'Codec', 'Stream'
        ]
        
        for var in categorical_variables:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df, x=var, y='Bitrate_Deviation_Percent', errorbar='se')
            plt.title(f'Correlation between {var} and Bitrate Deviation Percent')
            plt.xlabel(var)
            plt.ylabel('Bitrate Deviation Percent')
            plt.grid(True)
            
            # Make the directory if it doesn't exist
            if not os.path.exists(storage):
                os.makedirs(storage)
            
            plt.savefig(storage + f'bar_{var.lower()}_bitrate_deviation_percent.png')

    # Function to create and display the heatmap of correlations
    def plot_correlation_heatmap(df, storage="Measuring_Bitrate_Error/Plots/" + seconds + "_second/"):
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        correlation_matrix = df[numeric_columns].corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Matrix Heatmap')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        # Make the directory if it doesn't exist
        if not os.path.exists(storage):
            os.makedirs(storage)
        
        plt.savefig(storage + 'correlation_matrix_heatmap.png')

    # Creating the scatter plots for numeric variables
    create_scatter_plots(df)

    # Creating the bar plots for categorical variables
    create_bar_plots(df)

    # Plotting the correlation heatmap
    plot_correlation_heatmap(df)

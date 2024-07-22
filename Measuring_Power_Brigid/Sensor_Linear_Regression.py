import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def get_data():
    # Dictionary to store the dataframes
    data_frames = {}
    for fps in range(5, 31, 5):  # Adjust the range according to your files
        file_name = f'Data/encoder_30_sensor_{fps}.csv'
        df = pd.read_csv(file_name, names=['Timestamp', 'Value'], skiprows=1)
        df['Value'] = df['Value'] / 1000  # Convert microWatts to mW
        data_frames[fps] = df
    return data_frames

def perform_regression_and_plot(data_frames):
    fps_values = []
    means = []
    sems = []
    for fps, df in sorted(data_frames.items()):
        mean = df['Value'].mean()
        sem = df['Value'].sem()
        fps_values.append(fps)
        means.append(mean)
        sems.append(sem)
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(fps_values, means)
    
    # Prepare the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting each mean as a dot with SEM error bars
    ax.errorbar(fps_values, means, yerr=sems, fmt='o', label='Mean Power Consumption', capsize=5)
    
    # Plotting the line of best fit
    x_model = np.linspace(min(fps_values), max(fps_values), 100)
    y_model = intercept + slope * x_model
    ax.plot(x_model, y_model, 'r-', label=f'Line of Best Fit: y={intercept:.0f} + {slope:.0f}x')
    
    # Add R-squared value to the plot
    ax.text(0.05, 0.95, f'R-squared: {r_value**2:.2f}', transform=ax.transAxes, verticalalignment='top', fontsize=10)
    
    # Setting labels and title
    ax.set_xlabel('Sensor FPS')
    ax.set_ylabel('Mean Power Consumption (mW)')
    ax.set_title('Linear Regression of Power Consumption vs. Sensor FPS \n (Encoder FPS = 30)')
    ax.legend()

    # Show plot
    plt.show()
    
    # Print regression results
    print(f'Slope: {slope:.2f}')
    print(f'Intercept: {intercept:.2f}')
    print(f'R-squared: {r_value**2:.2f}')
    print(f'Std Error: {std_err:.2f}')
    print(f'p-value: {p_value:.3f}')

# Main execution
data_frames = get_data()
perform_regression_and_plot(data_frames)

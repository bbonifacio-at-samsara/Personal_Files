import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    # Read data directly from CSV files
    encoder_30_sensor_15_df = pd.read_csv('Data/encoder_30_sensor_15.csv', names=['Timestamp', 'Value'], skiprows=1)
    encoder_30_sensor_30_df = pd.read_csv('Data/encoder_30_sensor_30.csv', names=['Timestamp', 'Value'], skiprows=1)
    encoder_15_sensor_30_df = pd.read_csv('Data/encoder_15_sensor_30.csv', names=['Timestamp', 'Value'], skiprows=1)
    encoder_15_sensor_15_df = pd.read_csv('Data/encoder_15_sensor_15.csv', names=['Timestamp', 'Value'], skiprows=1)

    # Convert values to mW (currently in microWatts)
    for df in [encoder_30_sensor_15_df, encoder_30_sensor_30_df, encoder_15_sensor_30_df, encoder_15_sensor_15_df]:
        df['Value'] = df['Value'] / 1000

    # Return dataframes
    return encoder_30_sensor_15_df, encoder_30_sensor_30_df, encoder_15_sensor_30_df, encoder_15_sensor_15_df

# Retrieve the data
encoder_30_sensor_15_df, encoder_30_sensor_30_df, encoder_15_sensor_30_df, encoder_15_sensor_15_df = get_data()

def plot_histogram(data_15, data_30, title, ax):
    # Calculate the overall mean and SEM for each dataset
    mean_15, sem_15 = data_15['Value'].mean(), data_15['Value'].sem()
    mean_30, sem_30 = data_30['Value'].mean(), data_30['Value'].sem()

    # Calculate the base percentage difference between the means of the two datasets
    percent_difference = ((mean_30 - mean_15) / mean_15) * 100

    # Adjust the means by SEM for worst-case scenario calculations
    adjusted_mean_30_high = mean_30 + sem_30
    adjusted_mean_15_low = mean_15 - sem_15

    # Recalculate the percentage difference using the adjusted values
    adjusted_percent_difference = ((adjusted_mean_30_high - adjusted_mean_15_low) / adjusted_mean_15_low) * 100

    # Calculate the error associated with the original percent difference
    percent_difference_error = abs(adjusted_percent_difference - percent_difference)

    # Bar settings
    bar_width = 0.1
    index = [0, 0.15]

    # Plotting the bars with error bars for the means
    ax.bar(index[0], mean_15, yerr=sem_15, width=bar_width, label='15 FPS', color='skyblue', capsize=5)
    ax.bar(index[1], mean_30, yerr=sem_30, width=bar_width, label='30 FPS', color='salmon', capsize=5)

    # Setting labels and title
    ax.set_xlabel('FPS Setting')
    ax.set_ylabel('Mean Power Consumption (mW)')
    ax.set_title(f'{title} \nPercent Increase (15 -> 30): {percent_difference:.2f}% ± {percent_difference_error:.2f}%')
    ax.set_xticks(index)
    ax.set_xticklabels(['15 FPS', '30 FPS'])
    ax.set_ylim(0, max(mean_15 + sem_15, mean_30 + sem_30) * 1.1)  # Adjust y-axis limit

    # Annotate each bar with mean and SEM values
    ax.text(index[0], mean_15 + sem_15, f'Mean: {mean_15:.0f}\nSEM: {sem_15:.0f}', ha='center', va='bottom', color='black', fontsize=9)
    ax.text(index[1], mean_30 + sem_30, f'Mean: {mean_30:.0f}\nSEM: {sem_30:.0f}', ha='center', va='bottom', color='black', fontsize=9)

    ax.legend()

# Create figure and axes for the histograms
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# Plot histograms
plot_histogram(encoder_15_sensor_15_df, encoder_15_sensor_30_df, 'Encoder at 15 FPS: Sensor Power Comparison', axs[0, 0])
plot_histogram(encoder_30_sensor_15_df, encoder_30_sensor_30_df, 'Encoder at 30 FPS: Sensor Power Comparison', axs[0, 1])
plot_histogram(encoder_15_sensor_15_df, encoder_30_sensor_15_df, 'Sensor at 15 FPS: Encoder Power Comparison', axs[1, 0])
plot_histogram(encoder_15_sensor_30_df, encoder_30_sensor_30_df, 'Sensor at 30 FPS: Encoder Power Comparison', axs[1, 1])

plt.tight_layout()
plt.show()

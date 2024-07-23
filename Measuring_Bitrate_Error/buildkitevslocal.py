import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def process_data(csv_path, pattern):
    # Read and clean the data
    with open(csv_path, 'r') as file:
        data = file.read()
    cleaned_data = re.sub(pattern, '', data)
    data_lines = [line.split(', ') for line in cleaned_data.strip().split('\n')]

    # Create the DataFrame
    columns = [
        'Expected_Bytes', 'Actual_Bytes', 'Bitrate_Deviation_Percent', 'Duration_of_Experiment', 
        'Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 
        'Codec', 'Stream'
    ]
    df = pd.DataFrame(data_lines, columns=columns)

    # Convert appropriate columns to numeric
    df['Expected_Bytes'] = pd.to_numeric(df['Expected_Bytes'], errors='coerce')
    df['Actual_Bytes'] = pd.to_numeric(df['Actual_Bytes'], errors='coerce')
    df['Bitrate_Deviation_Percent'] = df['Bitrate_Deviation_Percent'].str.rstrip('%').astype(float)
    df['Duration_of_Experiment'] = pd.to_numeric(df['Duration_of_Experiment'], errors='coerce')

    # Group data and calculate stats
    grouped = df.groupby(['Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 'Codec', 'Stream'])
    summary = grouped['Bitrate_Deviation_Percent'].agg(['mean', 'std']).reset_index()
    summary['3x_std'] = summary['std'] * 3

    return summary

# Process data from both sources
local_csv = "Measuring_Bitrate_Error/Data/local/30_second.csv"
buildkite_csv = "Measuring_Bitrate_Error/Data/buildkite/30_second.csv"
local_summary = process_data(local_csv, r'functional_test\.go:974:\s*')
buildkite_summary = process_data(buildkite_csv, r'functional_test\.go:476:\s*')

# Merge the summaries for side-by-side comparison in the plot
merged_summary = pd.merge(local_summary, buildkite_summary, on=['Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 'Codec', 'Stream'], suffixes=('_local', '_buildkite'))

# Plotting
plt.figure(figsize=(15, 10), dpi=300)
width = 0.35  # Width of the bars
indices = range(len(merged_summary))
plt.bar(indices, merged_summary['mean_local'], width, yerr=merged_summary['3x_std_local'], label='Local', capsize=5)
plt.bar([i + width for i in indices], merged_summary['mean_buildkite'], width, yerr=merged_summary['3x_std_buildkite'], label='Buildkite', capsize=5)

# Add labels and legend
plt.xticks([i + width/2 for i in indices], merged_summary.apply(lambda row: f"{row['Resolution']}, {row['Bitrate_Control']}, {row['IDR_Interval']}, {row['Codec']}, {row['Stream']}, {row['Bitrate']}, {row['Framerate']}", axis=1), rotation=90)
plt.ylabel('Mean Bitrate Deviation Percent')
plt.xlabel('Unique Combinations')
plt.title('Comparison of Mean Bitrate Deviation Percent Between Local and Buildkite')
plt.axhline(y=15, color='r', linestyle='--', label='±15% Threshold')
plt.axhline(y=-15, color='r', linestyle='--')
plt.legend()
plt.grid(True)

# Save the plot
storage = "Measuring_Bitrate_Error/Plots/comparison/"
if not os.path.exists(storage):
    os.makedirs(storage)
plt.savefig(storage + 'comparison_mean_bitrate_deviation.png', bbox_inches='tight')
plt.show()

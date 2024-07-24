import pandas as pd
import re
import os

def process_and_save_csv(input_csv, output_csv):
    # Check if input CSV file exists
    if not os.path.exists(input_csv):
        print(f"No file found at {input_csv}")
        return

    # Read the CSV file
    with open(input_csv, 'r') as file:
        data = file.readlines()

    cleaned_data = []
    for line in data:
        # Remove the unwanted prefix and any surrounding whitespace
        cleaned_line = re.sub(r'functional_test\.go:\d+:\s*', '', line).strip()
        # Split the line into columns based on ', ' as delimiter
        columns = cleaned_line.split(', ')
        cleaned_data.append(columns)

    # Define the DataFrame columns based on your data structure
    column_names = [
        'Expected_Bytes', 'Actual_Bytes', 'Bitrate_Deviation_Percent', 'Duration_of_Experiment',
        'Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 
        'Codec', 'Stream'
    ]

    # Create a DataFrame
    df = pd.DataFrame(cleaned_data, columns=column_names)

    # Converting appropriate columns to numeric
    df['Expected_Bytes'] = pd.to_numeric(df['Expected_Bytes'], errors='coerce')
    df['Actual_Bytes'] = pd.to_numeric(df['Actual_Bytes'], errors='coerce')
    df['Bitrate_Deviation_Percent'] = df['Bitrate_Deviation_Percent'].str.rstrip('%').astype(float)
    df['Duration_of_Experiment'] = pd.to_numeric(df['Duration_of_Experiment'], errors='coerce')
    df['Bitrate'] = pd.to_numeric(df['Bitrate'], errors='coerce')
    df['Framerate'] = pd.to_numeric(df['Framerate'], errors='coerce')

    # Dropping any rows with NaN values that may have resulted from conversion errors
    df.dropna(inplace=True)

    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Processed data saved to {output_csv}")


input_csv_path = "Measuring_Bitrate_Error/Data/local_raw/30_second.csv"
output_csv_path = "Measuring_Bitrate_Error/Data/local_processed/30_second.csv"
process_and_save_csv(input_csv_path, output_csv_path)

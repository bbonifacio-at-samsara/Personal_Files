import pandas as pd
import re
import os

def process_raw_to_csv(input_dir, output_dir):
    # Walk through the input directory and process each file
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.txt'):  # Process only text files
                input_file = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(dirpath, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)

                # Ensure the output directory exists
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                output_file = os.path.join(output_subdir, filename.replace('.txt', '.csv'))
                process_file(input_file, output_file)

def process_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []

    for line in lines:
        # Remove the unwanted prefix
        cleaned_line = re.sub(r'functional_test\.go:\d+:\s*', '', line).strip()
        # Split the line on spaces and colons to extract the necessary information
        parts = re.split(':| ', cleaned_line)

        # Parse and calculate necessary fields
        codec = parts[0]
        stream = parts[1]
        resolution = parts[2]
        framerate = int(parts[3][4:])
        idr_interval = parts[4]
        bitrate_control = parts[5][:24]
        bitrate = int(parts[5][25:])
        actualBitrate = int(parts[11])
        bitrateDeviationPercent = float(parts[13].rstrip('%'))
        expected_bytes = bitrate * 30 / 8  # Example calculation for expected bytes

        # Append to data list
        data.append([
            expected_bytes, actualBitrate, bitrateDeviationPercent, 30, bitrate, framerate,
            resolution, bitrate_control, idr_interval, codec, stream
        ])

    # Create DataFrame
    columns = [
        'Expected_Bytes', 'Actual_Bytes', 'Bitrate_Deviation_Percent', 'Duration_of_Experiment', 
        'Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval', 
        'Codec', 'Stream'
    ]
    df = pd.DataFrame(data, columns=columns)

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)
    print(f"Data processed and saved to {output_file}")

# Example usage:
input_dir = 'Measuring_Bitrate_Error/Data/nightly_test_raw'
output_dir = 'Measuring_Bitrate_Error/Data/nightly_test_processed'
process_raw_to_csv(input_dir, output_dir)

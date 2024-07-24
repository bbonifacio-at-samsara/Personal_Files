import pandas as pd
import re

def process_raw_to_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []

    for line in lines:
        # Remove the unwanted prefix
        cleaned_line = re.sub(r'functional_test\.go:\d+:\s*', '', line).strip()
        
        # Split the line on spaces and colons to extract the necessary information
        parts = re.split(':| ', cleaned_line)
        print(parts)
        
        # Expected format: [Codec, Stream, Resolution, 'FPS', Framerate, 'IDR', IDR_Interval, 'BITRATE_CONTROL', Bitrate_Control, 'expectedFrames', Expected_Frames, 'actualFrames', Actual_Frames, 'actualBitrate', Actual_Bitrate, 'bitrateDeviation', Bitrate_Deviation_Percent]
        codec = parts[0]
        stream = parts[1]
        resolution = parts[2]
        framerate = int(parts[3][4:])
        idr_interval = parts[4]
        bitrate_control = parts[5][:24]
        bitrate = int(parts[5][25:])
        #expectedFrames = int(parts[7])
        #actualFrames = int(parts[9])
        actualBitrate = int(parts[11])
        bitrateDeviationPercent = float(parts[13].rstrip('%'))

        expected_bytes = bitrate * 30 /8

        # 437500, 131945, -69.84%, 1, 3500000, 30, RESOLUTION_2560X1440, BITRATE_CONTROL_CONSTANT, TWO, H265, CAMERA_PRIMARY
        # 'Expected_Bytes', 'Actual_Bytes', 'Bitrate_Deviation_Percent', 'Duration_of_Experiment',  'Bitrate', 'Framerate', 'Resolution', 'Bitrate_Control', 'IDR_Interval',  'Codec', 'Stream'
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


process_raw_to_csv('Measuring_Bitrate_Error/Data/nightly-test/real_data.txt', 'Measuring_Bitrate_Error/Data/nightly-test/real_data.csv')

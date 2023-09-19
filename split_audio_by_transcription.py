import csv
import os
import subprocess
from tqdm import tqdm

# Paths and filenames
input_audio_file = "/home/rgbellion/Documents/Projects/cceba-aproyo-prod/data/whisper.cpp/samples/sueño_2023-09-13_p4.wav"
csv_file = "/home/rgbellion/Documents/Projects/cceba-aproyo-prod/data/whisper.cpp/samples/sueño_2023-09-13_p4.wav.csv"
output_directory = "sueño_2023-09-13_p4"


if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Read the CSV file
with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Calculate the total number of chunks
    num_chunks = sum(1 for row in reader)

    # Reset the reader to the beginning of the CSV file
    csvfile.seek(0)
    next(reader)  # Skip the header row

    for row in tqdm(reader, total=num_chunks, desc="Processing chunks"):
        start_time = int(row['start']) / 1000  # Convert milliseconds to seconds
        end_time = int(row['end']) / 1000  # Convert milliseconds to seconds
        text = row['text'].strip()
        output_filename = os.path.join(output_directory, f"{text.replace(' ', '_')}.wav")

        # Use FFmpeg to extract the audio chunk
        cmd = [
            "ffmpeg",
            "-i", input_audio_file,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            output_filename
        ]

        subprocess.run(cmd)

"""

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read the CSV file
with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        start_time = int(row['start']) / 1000  # Convert milliseconds to seconds
        end_time = int(row['end']) / 1000  # Convert milliseconds to seconds
        text = row['text'].strip()
        output_filename = os.path.join(output_directory, f"{text.replace(' ', '_')}.wav")

        # Use FFmpeg to extract the audio chunk
        cmd = [
            "ffmpeg",
            "-i", input_audio_file,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            output_filename
        ]

        subprocess.run(cmd)

"""
print("Audio chunks extracted and saved in the"+ output_directory +" directory.")


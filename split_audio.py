import sys
import csv
import os
import subprocess
from tqdm import tqdm

def split_audio(input_audio_file):
    # Determine the CSV file name based on the input audio file name
    csv_file = f"{os.path.splitext(input_audio_file)[0]}.wav.csv"

    # Output directory based on the input audio file name
    output_directory = os.path.splitext(input_audio_file)[0]

    # Create the output directory if it doesn't exist
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

            # Create the directory for the output file if it doesn't exist
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)

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

    print(f"Audio chunks extracted and saved in the '{output_directory}' directory.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 split_audio.py <input_audio_file>")
        sys.exit(1)

    input_audio_file = sys.argv[1]
    split_audio(input_audio_file)


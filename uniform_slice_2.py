import argparse
import csv
import os
import subprocess

def slice_and_generate_text(input_audio, output_dir, duration):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract the base filename without extension
    base_filename = os.path.splitext(os.path.basename(input_audio))[0]

    # Generate the path to the CSV file
    csv_file = os.path.join(os.path.dirname(input_audio), f"{base_filename}.wav.csv")

    # Get the audio duration using FFmpeg
    ffprobe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_audio
    ]
    audio_duration = float(subprocess.check_output(ffprobe_cmd, universal_newlines=True))

    # Read the CSV file and store the text entries in a list
    text_entries = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text_entries.append((int(row['start']), row['text'].strip()))

    # Calculate the number of slices and duration in milliseconds
    num_slices = int(audio_duration / duration)
    slice_duration_ms = duration * 1000

    # Create audio slices and text files
    for i in range(num_slices):
        start_time_ms = i * slice_duration_ms
        end_time_ms = (i + 1) * slice_duration_ms

        # Filter text entries that correspond to this slice
        slice_text = ' '.join(entry[1] for entry in text_entries if start_time_ms <= entry[0] < end_time_ms)

        output_audio = os.path.join(output_dir, f"{base_filename}_{i + 1}.wav")
        cmd = [
            "ffmpeg",
            "-i", input_audio,
            "-ss", str(start_time_ms / 1000),
            "-to", str(end_time_ms / 1000),
            "-c", "copy",
            output_audio
        ]
        subprocess.run(cmd)

        # Create the text file for this slice
        output_txt = os.path.join(output_dir, f"{base_filename}_{i + 1}.txt")
        with open(output_txt, 'w', encoding='utf-8') as txtfile:
            txtfile.write(slice_text)

def main():
    parser = argparse.ArgumentParser(description="Slice audio and generate concatenated text files.")
    parser.add_argument("-d", "--duration", type=int, required=True, help="Duration of each audio slice in seconds.")
    parser.add_argument("-i", "--input_audio", required=True, help="Input audio file (e.g., audio1.wav).")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory for audio slices and text files.")

    args = parser.parse_args()

    slice_and_generate_text(args.input_audio, args.output_dir, args.duration)

if __name__ == "__main__":
    main()


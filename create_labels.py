import csv
import os
import sys

def create_text_files(csv_file, output_path):
    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"CSV file '{csv_file}' not found.")
        return

    # Read the CSV file
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            text = row['text'].strip()
            txt_filename = f"{text.replace(' ', '_')}.txt"
            txt_filepath = os.path.join(output_path, txt_filename)

            # Create and write the text content to the txt file
            with open(txt_filepath, 'w', encoding='utf-8') as txtfile:
                txtfile.write(text)

    print(f"Text files created in the '{output_path}' directory.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 create_text_files.py <csv_file> <output_path>")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    create_text_files(csv_file, output_path)


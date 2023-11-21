#!/usr/bin/env python3
import argparse
import csv
import logging
import os.path
import sys

logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(input_directory: str, output_directory: str, output_file: str, col: str, row: str):
    # Validating input directory
    if not os.path.isabs(input_directory):
        input_path = os.path.join(os.getcwd(), input_directory)
    else:
        input_path = input_directory
    input_path = os.path.normpath(input_path)
    if not os.path.exists(input_path) or not os.path.isdir(input_path):
        logger.error("Input directory does not exist")
        sys.exit(1)

    # Validating output directory
    if not os.path.isabs(output_directory):
        output_path = os.path.join(os.getcwd(), output_directory)
    else:
        output_path = output_directory
    if not os.path.exists(output_path) or not os.path.isdir(output_path):
        logger.error("Output directory does not exist")
        sys.exit(1)

    # If there is not an output file specified, then take the name from the input directory
    if not output_file:
        output_file = f"{os.path.split(input_path)[1]}.csv"
    output_file = os.path.normpath(os.path.join(output_path, output_file))

    logger.info(f"Transposing files in `{input_path}` and saving to `{output_file}`")

    all_keys = set()
    files_data = []
    for input_file in next(os.walk(input_path), (None, None, []))[2]:
        input_file_path = os.path.join(input_path, input_file)
        ext = os.path.splitext(input_file_path)[-1].lower()

        # Ignore anything which is not .txt or .csv file
        if ext not in ['.csv', '.txt']:
            continue

        logger.info(f"\tTransposing: `{input_file}`")

        # TODO: Better encoding handling needed here, or potentially consider reading
        #  as bytes and doing the CSV bit by hand
        process_file = True
        with open(input_file_path, 'r', encoding='UTF-16', newline='') as csvfile:
            rows = []
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            for csv_row in csvreader:
                # Transform data to strip leading/trailing chars
                transform_data = {key.strip(): value.strip() for key, value in csv_row.items()}

                if col not in transform_data:
                    logger.warning(f"Unable to process file as column `{col}` is missing")
                    process_file = False
                    break
                if row not in transform_data:
                    logger.warning(f"Unable to process file as column `{row}` is missing")
                    process_file = False
                    break
                rows.append(transform_data)

        if process_file:
            file_data = {}
            for file_row in rows:
                if file_row[col] in file_data:
                    logger.warning(f"Unable to process file as column `{file_row[col]}` appears more "
                                   f"than once")
                    process_file = False
                    break
                file_data[file_row[col]] = file_row[row]

            if process_file:
                files_data.append(file_data)
                for key in file_data.keys():
                    all_keys.add(key)

    # TODO: Might need better encoding handling here - setting to UTF-16 to match input data
    with open(output_file, 'w', encoding='UTF-16', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(list(all_keys)), delimiter='\t')
        writer.writeheader()
        for file_data in files_data:
            data_to_write = {key: file_data.get(key, '') for key in all_keys}
            writer.writerow(data_to_write)

    logger.info("Finished transposing and written to output file")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='csv-transpose',
        description='Transpose a directory of CSV files into a single output file'
    )
    arg_parser.add_argument('input_directory')
    arg_parser.add_argument('output_directory')
    arg_parser.add_argument('--output_file', default=None)
    arg_parser.add_argument('--col', default='Name')
    arg_parser.add_argument('--row', default='Value')

    args = arg_parser.parse_args()
    main(args.input_directory, args.output_directory, args.output_file, args.col, args.row)

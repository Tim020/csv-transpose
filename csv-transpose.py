#!/usr/bin/env python3
import argparse
import logging
import os.path
import sys

logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(input_directory: str, output_directory: str, output_file: str):
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
    output_file = os.path.normpath(os.path.join(output_path, output_file))

    logger.info(f"Transposing files in {input_path} and saving to {output_file}")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='csv-transpose',
        description='Transpose a directory of CSV files into a single output file'
    )
    arg_parser.add_argument('input_directory')
    arg_parser.add_argument('output_directory')
    arg_parser.add_argument('--output_file', default='output.csv')

    args = arg_parser.parse_args()
    main(args.input_directory, args.output_directory, args.output_file)

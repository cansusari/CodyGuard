from looker_cody_guard import LookerCodyGuard
import itertools
import argparse
import logging
import lkml
import sys
import re
import os


if __name__ == "__main__":
    # Logging Configurations
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("Looker Cody Guard is running!")

    # Path configuration
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Get Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file_path', default=None, help='File Path (default = None)')
    args = parser.parse_args()

    logging.info(f"Parameters: {args}")

    # Define Variables 
    file_path = args.file_path

    # Create an instance of LookerCodyGuard Class
    lg = LookerCodyGuard()
    logging.info('File path: ' + file_path)
    hasError = lg.check_file(file_path=file_path)

    if hasError != '':
        logging.error('There is a validation error!')
        logging.error(hasError)
        sys.exit(1)
    else:
        logging.info('There is no validation error!')
        sys.exit(0)



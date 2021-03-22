#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# Author: Max Nowak

from docopt import docopt

import data_purifier

__doc__ = \
    """
    Usage:
          cli_data_purifier.py <filename> [-s | --sliced]
          cli_data_purifier.py -h | --help
        
        Options:
          -h --help             Show this screen.
          -s --sliced           Return only relevant digits [3:6)
    """

args = docopt(__doc__)

if args['--help']:
    """Prints the usage as help."""
    print(__doc__)

if args['filename']:
    """Returns data from csv file."""
    try:
        if args['sliced']:
            data = data_purifier.extract_sliced_clean_data(args['filename'])
        else:
            data = data_purifier.extract_clean_data(args['filename'])
    except Exception as e:
        print('Something went wrong: ' + str(e))
    else:
        print(data)

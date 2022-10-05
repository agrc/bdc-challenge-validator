#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

import sys

import pandas as pd

from . import checks


def process(csv_path):
    dataframe = pd.read_csv(csv_path, dtype=str)

    matching_cols, missing_cols, extra_cols = checks.column_name_check(dataframe)
    error = False
    nt = '\n\t'
    matching_message = f'Valid columns:{nt}{nt.join(sorted(matching_cols))}'
    if missing_cols:
        error = True
        missing_message = f'Missing required columns:{nt}{nt.join(sorted(missing_cols))}'
    if extra_cols:
        error = True
        extra_message = f'Columns that should be renamed or removed:{nt}{nt.join(sorted(extra_cols))}'
    if error:
        print('\n**Invalid column names**\n')
        print(matching_message)
        print(missing_message)
        print(extra_message)
        print('Please fix the column names and run again')
        return

    dataframe['category_code'] == dataframe['category_code'].astype(int)


def main():
    process(r'C:\gis\Projects\BroadbandFabric\working data\Wayne\wayne.csv')


if __name__ == '__main__':
    #: the code that executes if you run the file or module directly
    process(r'C:\gis\Projects\BroadbandFabric\working data\Wayne\wayne.csv')

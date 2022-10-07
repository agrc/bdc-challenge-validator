#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

from pathlib import Path

import pandas as pd

from . import checks


def _print_header(message):
    # print('-' * 40)
    print(f'\n\n{message:^40}')
    print('-' * 40)


def _all_elements_equal(dataframe, value):
    a = dataframe.to_numpy()
    return (value == a).all(0).all()


def _move_result_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    new_columns = []
    existing_columns = list(dataframe.columns)
    for column in existing_columns:
        new_columns.append(column)
        if f'{column}_result' in existing_columns:
            new_columns.append(f'{column}_result')
            existing_columns.remove(f'{column}_result')

    return dataframe.reindex(columns=new_columns)


def process(csv_path):
    dataframe = pd.read_csv(csv_path, dtype=str)

    _print_header('Checking column names')
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
    print('Valid')

    _print_header('Checking category codes')
    dataframe, category_code_result = checks.category_code_check(dataframe)
    print(category_code_result)
    if dataframe is None:
        print('Please fix category codes and run again')
        return

    _print_header('Checking other columns')
    columns_to_check = [
        'location_id',
        'address_primary',
        'city',
        'state',
        'zip_code',
        'zip_code_suffix',
        'unit_count',
        'building_type_code',
        'non_bsl_code',
        'bsl_lacks_address_flag',
        'latitude',
        'longitude',
    ]
    results_df = pd.DataFrame()

    for column in columns_to_check:
        print(f'{column}...')
        exec(f'results_df[\'{column}_result\'] = dataframe.apply(checks.{column}_check, axis=1)')

    if not _all_elements_equal(results_df, 'Valid'):
        csv_path = Path(csv_path)
        new_path = csv_path.parent / f'{csv_path.stem}_results.csv'
        print(f'Errors detected. Results written to {new_path}')
        combined_dataframe = _move_result_columns(dataframe.join(results_df))
        combined_dataframe.to_csv(new_path)
        return

    _print_header('All checks completed, file is valid')
    return


def main():
    process(r'C:\gis\Projects\BroadbandFabric\working data\Wayne\wayne_bad_category_codes.csv')


if __name__ == '__main__':
    #: the code that executes if you run the file or module directly
    process(r'C:\gis\Projects\BroadbandFabric\working data\Wayne\wayne_bad_category_codes.csv')

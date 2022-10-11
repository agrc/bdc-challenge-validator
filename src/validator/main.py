#!/usr/bin/env python
# * coding: utf8 *
"""
A quick module for checking whether a csv, shapefile, or feature class conforms to the FCC's Broadband Data Collection
Bulk Data Challenge format.
"""

import sys
from pathlib import Path

import pandas as pd
from arcgis import GeoAccessor, GeoSeriesAccessor

from . import checks


def _print_header(message):
    # print('-' * 40)
    print(f'\n\n{message:^40}')
    print('-' * 40)


def _load_data(input_path):
    # input_path = Path(fr'{input_path}')

    try:
        if input_path.suffix == '.csv':
            return pd.read_csv(input_path, dtype=str).fillna('')
        if input_path.suffix == '.shp' or input_path.parts[-2][-4:] == '.gdb':
            raise NotImplementedError('Shapefile and feature class reading not yet implemented')
            #: TODO: handle converting everything to strings, handling empty values, etc from spatial dfs
            # return pd.DataFrame.spatial.from_featureclass(input_path).fillna('')
    except (OSError, KeyError, FileNotFoundError):
        print(f'Could not open {input_path}. Please check the filename and try again.')

    #: If we don't get a csv, shapefile, or featureclass, print a notice and return None
    # print('CSV, Shapefile, or Feature Class required. Please check your input path and try again.')
    print('CSV required. Please check your input path and try again.')
    return None


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


def _write_results_dataframe(input_path, combined_dataframe):
    parent = input_path.parent
    if input_path.parent.suffix == '.gdb':
        parent = input_path.parent.parent
    new_path = parent / f'{input_path.stem}_validator_results.csv'
    print(f'Errors detected. Results written to {new_path}')
    combined_dataframe.to_csv(new_path)


def process(input_path):

    input_path = Path(input_path)

    _print_header(f'Reading in {input_path}')
    dataframe = _load_data(input_path)
    if dataframe is None:
        return

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
        'contact_name',
        'contact_email',
        'contact_phone',
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

    _print_header('Results')

    if not _all_elements_equal(results_df, 'Valid'):
        combined_dataframe = _move_result_columns(dataframe.join(results_df))
        _write_results_dataframe(input_path, combined_dataframe)
        return

    _print_header('All checks completed, file is valid')
    return


def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        print('Must specify the path to the file to be validated.')
        sys.exit()
    if len(sys.argv) > 2:
        print('Only one file may be specified (check for unescaped spaces in path).')
        sys.exit()
    process(sys.argv[1])


if __name__ == '__main__':
    main()

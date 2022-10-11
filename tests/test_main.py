from pathlib import Path

import numpy as np
import pandas as pd
from pandas import testing as tm

from validator import main


def test_move_result_columns():
    df = pd.DataFrame(columns=['category_code', 'location_id', 'something', 'location_id_result'])

    new_df = main._move_result_columns(df)

    test_df = pd.DataFrame(columns=['category_code', 'location_id', 'location_id_result', 'something'])

    tm.assert_frame_equal(new_df, test_df)


def test_all_elements_equal_returns_true_for_all_equal():
    df = pd.DataFrame({'foo': ['bar', 'bar'], 'baz': ['bar', 'bar']})

    results = main._all_elements_equal(df, 'bar')

    assert results


def test_all_elements_equal_returns_false_for_some_equal():
    df = pd.DataFrame({'foo': ['bar', 'bar'], 'baz': ['bar', 'boo']})

    results = main._all_elements_equal(df, 'bar')

    assert not results


def test_all_elements_equal_returns_false_for_all_unique():
    df = pd.DataFrame({'foo': ['bar', 'boo'], 'baz': ['eggs', 'ham']})

    results = main._all_elements_equal(df, 'bar')

    assert not results


def test_load_data_fills_na_from_csv(mocker):
    csv_df = pd.DataFrame({
        'a': ['1', '2'],
        'b': ['3', np.nan],
    })
    mocker.patch('validator.main.pd.read_csv', return_value=csv_df)

    result_df = main._load_data(Path(r'c:\temp\foo.csv'))

    test_df = pd.DataFrame({
        'a': ['1', '2'],
        'b': ['3', ''],
    })

    tm.assert_frame_equal(result_df, test_df)


def test_write_results_dataframe_builds_path_input_csv(mocker):
    mock_df = mocker.Mock()

    input_path = Path(r'c:\foo\bar\baz.csv')
    main._write_results_dataframe(input_path, mock_df)

    mock_df.to_csv.assert_called_with(Path(r'c:\foo\bar\baz_validator_results.csv'))


def test_write_results_dataframe_builds_path_input_featureclass(mocker):
    mock_df = mocker.Mock()

    input_path = Path(r'c:\foo\bar.gdb\baz')
    main._write_results_dataframe(input_path, mock_df)

    mock_df.to_csv.assert_called_with(Path(r'c:\foo\baz_validator_results.csv'))

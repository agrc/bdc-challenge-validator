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

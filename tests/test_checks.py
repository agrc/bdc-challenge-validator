import pandas as pd
from pandas import testing as tm

import validator
from validator import checks

# def test_category_codes():

#     rows = [{'category_code': foo} for foo in range(0, 9)]

#     output = []
#     for row in rows:
#         output.append(checks.category_code_check(row))

#     test_output = [
#         'Invalid category_code', 'Valid', 'Valid', 'Valid', 'Valid', 'Valid', 'Valid', 'Valid', 'Invalid category_code'
#     ]

#     assert output == test_output


def test_category_code_check_casts_to_int():
    df = pd.DataFrame({
        'category_code': ['1', '2', '3', '4', '5', '6', '7'],
    })

    dataframe, result = checks.category_code_check(df)

    test_df = pd.DataFrame({
        'category_code': [1, 2, 3, 4, 5, 6, 7],
    })

    assert result == 'Valid'
    tm.assert_frame_equal(dataframe, test_df)


def test_category_code_check_str_in_df():
    df = pd.DataFrame({
        'category_code': ['1', '2', '3', '4', '5', '6', 'foo'],
    })

    dataframe, result = checks.category_code_check(df)

    assert not dataframe
    assert result == 'Non-integer, non-numeric or empty category_code values present'


def test_category_code_check_empty_str_in_df():
    df = pd.DataFrame({
        'category_code': ['1', '2', '3', '4', '5', '6', ''],
    })

    dataframe, result = checks.category_code_check(df)

    assert not dataframe
    assert result == 'Non-integer, non-numeric or empty category_code values present'


def test_category_code_check_float_in_df():
    df = pd.DataFrame({
        'category_code': ['1', '2', '3', '4', '5', '6', '7.0'],
    })

    dataframe, result = checks.category_code_check(df)

    assert not dataframe
    assert result == 'Non-integer, non-numeric or empty category_code values present'


def test_category_code_check_value_under_range():
    df = pd.DataFrame({
        'category_code': ['1', '2', '3', '4', '5', '6', '0'],
    })

    dataframe, result = checks.category_code_check(df)

    assert not dataframe
    assert result == 'One or more category codes were not between 1 and 7.'


def test_category_code_check_value_over_range():
    df = pd.DataFrame({
        'category_code': ['1', '2', '3', '4', '5', '6', '10'],
    })

    dataframe, result = checks.category_code_check(df)

    assert not dataframe
    assert result == 'One or more category codes were not between 1 and 7.'


def test_contact_name_check():
    # yapf: disable
    rows = [
        {'contact_name': ''},
        {'contact_name': 'Foo Bar'},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.contact_name_check(row))

    test_output = [
        'contact_name must include the name of the person preparing the challenge',
        'Valid',
    ]

    assert output == test_output


def test_contact_email_check():
    # yapf: disable
    rows = [
        {'contact_email': ''},
        {'contact_email': 'missing_at_foo.com'},
        {'contact_email': 'missing@thedot'},
        {'contact_email': 'missing_at_foo.com'},
        {'contact_email': 'missingafter@'},
        {'contact_email': 'valid@foo.com'},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.contact_email_check(row))

    test_output = [
        'contact_email must be included and have the form someone@somewhere.sometld',
        'contact_email must be included and have the form someone@somewhere.sometld',
        'contact_email must be included and have the form someone@somewhere.sometld',
        'contact_email must be included and have the form someone@somewhere.sometld',
        'contact_email must be included and have the form someone@somewhere.sometld',
        'Valid',
    ]

    assert output == test_output


def test_contact_phone_check():
    # yapf: disable
    rows = [
        {'contact_phone': '111-222-3333'},
        {'contact_phone': '1112223333'},
        {'contact_phone': '(111) 222-3333'},
        {'contact_phone': '111-222-333'},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.contact_phone_check(row))

    test_output = [
        'Valid',
        'contact_phone must be in format xxx-yyy-zzzz',
        'contact_phone must be in format xxx-yyy-zzzz',
        'contact_phone must be in format xxx-yyy-zzzz',
    ]

    assert output == test_output


def test_location_id_check_format():
    # yapf: disable
    rows = [
        {'location_id': '123456', 'category_code': -1},
        {'location_id': 'string', 'category_code': -1},
        {'location_id': '123withstring', 'category_code': -1},
        {'location_id': '1234567890', 'category_code': -1}
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.location_id_check(row))

    test_output = [
        'location_id must be a 10-digit number',
        'location_id must be a 10-digit number',
        'location_id must be a 10-digit number',
        'Valid',
    ]

    assert output == test_output


def test_location_id_check_category_code_checks():
    # yapf: disable
    rows = [
        {'location_id': '1234567890', 'category_code': 1},
        {'location_id': '1234567890', 'category_code': 2},
        {'location_id': '', 'category_code': 1},
        {'location_id': '', 'category_code': 2}
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.location_id_check(row))

    test_output = [
        'location_id must be empty for category_code 1',
        'Valid',
        'Valid',
        'location must be included for category_code 2-7',
    ]

    assert output == test_output


def test_address_primary_check():
    # yapf: disable
    rows = [
        {'address_primary': '', 'category_code': 7},
        {'address_primary': '', 'category_code': 2, 'bsl_lacks_address_flag': 0},
        {'address_primary': '', 'category_code': 2, 'bsl_lacks_address_flag': 1},
        {'address_primary': '', 'category_code': 3},
        {'address_primary': 'addr', 'category_code': 3},
        {'address_primary': 'addr', 'category_code': 2, 'bsl_lacks_address_flag': 1},
        {'address_primary': 'addr', 'category_code': 2, 'bsl_lacks_address_flag': 0},
        {'address_primary': 'addr', 'category_code': 7},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.address_primary_check(row))

    test_output = [
        'address_primary required for category_code 7',
        'address_primary required for category codes 1 or 2 with bsl_lacks_address_flag set to 0',
        'Valid',
        'Valid',
        'address_primary must be empty for category_codes 3-6',
        'address_primary must be empty for category codes 1 or 2 with bsl_lacks_address_flag set to 1',
        'Valid',
        'Valid',
    ]

    assert output == test_output


def test_city_check():
    # yapf: disable
    rows = [
        {'city': 'foo', 'category_code': 3},
        {'city': 'foo', 'category_code': 1},
        {'city': '', 'category_code': 1},
        {'city': '', 'category_code': 3},

    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.city_check(row))

    test_output = [
        'city must be empty for category codes 3-6',
        'Valid',
        'city required for category codes 1, 2, or 7',
        'Valid',
    ]

    assert output == test_output


def test_state_check():
    # yapf: disable
    rows = [
        {'state': 'UT', 'category_code': 3},
        {'state': 'UT', 'category_code': 1},
        {'state': 'ZZ', 'category_code': 1},
        {'state': '', 'category_code': 1},
        {'state': '', 'category_code': 3},

    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.state_check(row))

    test_output = [
        'state must be empty for category codes 3-6',
        'Valid',
        'state must be UT',
        'state required for category codes 1, 2, or 7',
        'Valid',
    ]

    assert output == test_output


def test_zip_check():
    # yapf: disable
    rows = [
        {'zip_code': '', 'category_code': 7},
        {'zip_code': '', 'category_code': 2, 'bsl_lacks_address_flag': 0},
        {'zip_code': '', 'category_code': 2, 'bsl_lacks_address_flag': 1},
        {'zip_code': '', 'category_code': 3},
        {'zip_code': '84093', 'category_code': 3},
        {'zip_code': '84093', 'category_code': 2, 'bsl_lacks_address_flag': 1},
        {'zip_code': '84093', 'category_code': 2, 'bsl_lacks_address_flag': 0},
        {'zip_code': '84093', 'category_code': 7},
        {'zip_code': '840932', 'category_code': 7},
        {'zip_code': '8409', 'category_code': 7},
        {'zip_code': 'str', 'category_code': 7},



    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.zip_code_check(row))

    test_output = [
        'zip_code required for category_code 7',
        'zip_code required for category codes 1 or 2 with bsl_lacks_address_flag set to 0',
        'Valid',
        'Valid',
        'zip_code must be empty for category_codes 3-6',
        'Valid',
        'Valid',
        'Valid',
        'zip_code must in the form 84xyz',
        'zip_code must in the form 84xyz',
        'zip_code must in the form 84xyz',
    ]

    assert output == test_output


def test_zip_code_suffix_check():
    # yapf: disable
    rows = [
        {'zip_code_suffix': '1234', 'category_code': 3},
        {'zip_code_suffix': '1234', 'category_code': 1},
        {'zip_code_suffix': '', 'category_code': 1},
        {'zip_code_suffix': '', 'category_code': 3},
        {'zip_code_suffix': 'abc', 'category_code': 1},
        {'zip_code_suffix': '12345', 'category_code': 1},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.zip_code_suffix_check(row))

    test_output = [
        'zip_code_suffix must be empty for category_codes 3-6',
        'Valid',
        'Valid',
        'Valid',
        'zip_code_suffix must be a four-digit number',
        'zip_code_suffix must be a four-digit number',
    ]

    assert output == test_output


def test_unit_count_check():
    # yapf: disable
    rows = [
        {'unit_count': '', 'category_code': 1},
        {'unit_count': '4', 'category_code': 1},
        {'unit_count': '', 'category_code': 2},
        {'unit_count': '4', 'category_code': 2},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.unit_count_check(row))

    test_output = [
        'unit_count required for category codes 1 and 3',
        'Valid',
        'Valid',
        'unit_count must be empty for category codes 2, 4, 5, 6, 7',
    ]

    assert output == test_output


def test_building_type_code_check():
    # yapf: disable
    rows = [
        {'building_type_code': 'B', 'category_code': 2},
        {'building_type_code': 'B', 'category_code': 1},
        {'building_type_code': 'Y', 'category_code': 2},
        {'building_type_code': 'Y', 'category_code': 1},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.building_type_code_check(row))

    test_output = [
        'building_type_code must be empty for category codes 2, 3, 5, 6, 7',
        'Valid',
        'building_type_code must be empty for category codes 2, 3, 5, 6, 7',
        'building_type_code must be B, R, X, G, C, or E for category codes 1 and 4',
    ]

    assert output == test_output


def test_non_bsl_code_check():
    # yapf: disable
    rows = [
        {'non_bsl_code': 'S', 'category_code': 1},
        {'non_bsl_code': 'S', 'category_code': 6},
        {'non_bsl_code': 'Y', 'category_code': 1},
        {'non_bsl_code': 'Y', 'category_code': 6},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.non_bsl_code_check(row))

    test_output = [
        'non_bsl_code must be empty for category codes 1, 2, 3, 4, 5, 7',
        'Valid',
        'non_bsl_code must be empty for category codes 1, 2, 3, 4, 5, 7',
        'non_bsl_code must be S, L, G, H, F, E, P, N, or R for category code 6',
    ]

    assert output == test_output


def test_bsl_lacks_address_flag_check():
    # yapf: disable
    rows = [
        {'bsl_lacks_address_flag': '1', 'category_code': 1},
        {'bsl_lacks_address_flag': '10', 'category_code': 1},
        {'bsl_lacks_address_flag': '', 'category_code': 1},
        {'bsl_lacks_address_flag': '1', 'category_code': 3},
        {'bsl_lacks_address_flag': '', 'category_code': 3},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.bsl_lacks_address_flag_check(row))

    test_output = [
        'Valid',
        'bsl_lacks_address_flag must have a value of 0 or 1 for category code 1 or 2',
        'bsl_lacks_address_flag must have a value of 0 or 1 for category code 1 or 2',
        'bsl_lacks_address_flag must be empty for category codes 3-7',
        'Valid',
    ]

    assert output == test_output


def test_latitude_check():
    # yapf: disable
    rows = [
        {'latitude': '30.000000', 'category_code': 1},
        {'latitude': '40.000000', 'category_code': 1},
        {'latitude': '50.000000', 'category_code': 1},
        {'latitude': '40.000000', 'category_code': 2},
        {'latitude': '', 'category_code': 2},
        {'latitude': '40.0000', 'category_code': 1},
        {'latitude': '40.000000000', 'category_code': 1},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.latitude_check(row))

    test_output = [
        'latitude out of range 36.8 to 42.2',
        'Valid',
        'latitude out of range 36.8 to 42.2',
        'latitude must be empty for category codes 2, 3, 4, 6, 7',
        'Valid',
        'latitude must have a minimum precision of 6 decimal places',
        'Valid',
    ]

    assert output == test_output


def test_longitude_check():
    # yapf: disable
    rows = [
        {'longitude': '-120.000000', 'category_code': 1},
        {'longitude': '-110.000000', 'category_code': 1},
        {'longitude': '-100.000000', 'category_code': 1},
        {'longitude': '-110.000000', 'category_code': 2},
        {'longitude': '', 'category_code': 2},
        {'longitude': '-110.0000', 'category_code': 1},
        {'longitude': '-110.000000000', 'category_code': 1},
    ]
    # yapf: enable

    output = []
    for row in rows:
        output.append(checks.longitude_check(row))

    test_output = [
        'longitude out of range -114.3 to -109',
        'Valid',
        'longitude out of range -114.3 to -109',
        'longitude must be empty for category codes 2, 3, 4, 6, 7',
        'Valid',
        'longitude must have a minimum precision of 6 decimal places',
        'Valid',
    ]

    assert output == test_output


def test_column_name_check_all_good_names():
    test_df = pd.DataFrame(
        columns=[
            'contact_name',
            'contact_email',
            'contact_phone',
            'category_code',
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
    )

    matching, missing, extra = checks.column_name_check(test_df)

    assert matching == {
        'contact_name',
        'contact_email',
        'contact_phone',
        'category_code',
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
    }
    assert not missing
    assert not extra


def test_column_name_check_missing_and_extra():
    test_df = pd.DataFrame(
        columns=[
            'contact_name',
            'contact_email',
            'contact_phone',
            'category_code',
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
            'extralongitude',
        ]
    )

    matching, missing, extra = checks.column_name_check(test_df)

    assert matching == {
        'contact_name',
        'contact_email',
        'contact_phone',
        'category_code',
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
    }
    assert missing == {'longitude'}
    assert extra == {'extralongitude'}

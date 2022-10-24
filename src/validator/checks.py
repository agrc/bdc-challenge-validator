import re

import pandas as pd


def column_name_check(dataframe):
    good_column_names = {
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

    dataframe_column_names = set(dataframe.columns)

    matched_names = good_column_names & dataframe_column_names
    missing_good_names = good_column_names - dataframe_column_names
    extra_dataframe_names = dataframe_column_names - good_column_names

    return (matched_names, missing_good_names, extra_dataframe_names)


def category_code_check(dataframe):

    try:
        dataframe['category_code'] = dataframe['category_code'].astype('int64')
    except ValueError:
        return None, 'Non-integer, non-numeric or empty category_code values present'

    if not dataframe['category_code'].between(1, 7).all():
        return None, 'One or more category codes were not between 1 and 7.'

    return dataframe, 'Valid'


def contact_name_check(row):
    if not row['contact_name']:
        return 'contact_name must include the name of the person preparing the challenge'
    return 'Valid'


def contact_email_check(row):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', row['contact_email']):
        return 'contact_email must be included and have the form someone@somewhere.sometld'
    return 'Valid'


def contact_phone_check(row):
    if row['contact_phone'] and not re.search('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', row['contact_phone']):
        return 'contact_phone must be in format xxx-yyy-zzzz'
    return 'Valid'


def location_id_check(row):
    #: need to make sure we clean up any blank/empty strings in 'location_id'first.
    #: '<Null>'s may need to be cleaned up as well.
    #: need to make sure this is loaded as a string

    if row['location_id']:
        if not re.search('^[0-9]{10}$', row['location_id']):
            return 'location_id must be a 10-digit number'

        if row['category_code'] == 1:
            return 'location_id must be empty for category_code 1'

    if not row['location_id'] and row['category_code'] != 1:
        return 'location must be included for category_code 2-7'

    return 'Valid'


def address_primary_check(row):

    if not row['address_primary']:
        if row['category_code'] == 7:
            return 'address_primary required for category_code 7'
        if row['category_code'] in (1, 2) and row['bsl_lacks_address_flag'] == '0':
            return 'address_primary required for category codes 1 or 2 with bsl_lacks_address_flag set to 0'

    if row['address_primary']:
        if row['category_code'] in (3, 4, 5, 6):
            return 'address_primary must be empty for category_codes 3-6'
        if row['category_code'] in (1, 2) and row['bsl_lacks_address_flag'] == '1':
            return 'address_primary must be empty for category codes 1 or 2 with bsl_lacks_address_flag set to 1'

    return 'Valid'


def city_check(row):
    if row['city'] and row['category_code'] in (3, 4, 5, 6):
        return 'city must be empty for category codes 3-6'
    if not row['city'] and row['category_code'] in (1, 2, 7):
        return 'city required for category codes 1, 2, or 7'

    return 'Valid'


def state_check(row, state_code='UT'):

    if row['state'] and row['category_code'] in (3, 4, 5, 6):
        return 'state must be empty for category codes 3-6'
    if not row['state'] and row['category_code'] in (1, 2, 7):
        return 'state required for category codes 1, 2, or 7'
    if row['state'] and row['state'] != state_code:
        return f'state must be {state_code}'
    return 'Valid'


def zip_code_check(row, zip_prefix='84'):

    if not row['zip_code']:
        if row['category_code'] == 7:
            return 'zip_code required for category_code 7'
        if row['category_code'] in (1, 2) and row['bsl_lacks_address_flag'] == '0':
            return 'zip_code required for category codes 1 or 2 with bsl_lacks_address_flag set to 0'

    if row['zip_code'] and row['category_code'] in (3, 4, 5, 6):
        return 'zip_code must be empty for category_codes 3-6'

    pattern = '^' + zip_prefix + '[0-9]{3}$'
    if row['zip_code'] and not re.match(pattern, row['zip_code']):
        return f'zip_code must in the form {zip_prefix}xyz'

    return 'Valid'


def zip_code_suffix_check(row):
    if row['zip_code_suffix'] and row['category_code'] in (3, 4, 5, 6):
        return 'zip_code_suffix must be empty for category_codes 3-6'

    if row['zip_code_suffix'] and not re.match('^[0-9]{4}$',
                                               row['zip_code_suffix']) and row['category_code'] not in (3, 4, 5, 6):
        return 'zip_code_suffix must be a four-digit number'

    return 'Valid'


def unit_count_check(row):
    if not row['unit_count'] and row['category_code'] in (1, 3):
        return 'unit_count required for category codes 1 and 3'
    if row['unit_count'] and row['category_code'] in (2, 4, 5, 6, 7):
        return 'unit_count must be empty for category codes 2, 4, 5, 6, 7'
    return 'Valid'


def building_type_code_check(row):
    allowed_values = ('B', 'R', 'X', 'G', 'C', 'E')
    if row['building_type_code'] and row['category_code'] in (2, 3, 5, 6, 7):
        return 'building_type_code must be empty for category codes 2, 3, 5, 6, 7'
    if row['category_code'] in (1, 4) and row['building_type_code'] not in allowed_values:
        return 'building_type_code must be B, R, X, G, C, or E for category codes 1 and 4'
    return 'Valid'


def non_bsl_code_check(row):
    allowed_values = ('S', 'L', 'G', 'H', 'F', 'E', 'P', 'N', 'R')
    if row['non_bsl_code'] and row['category_code'] in (1, 2, 3, 4, 5, 7):
        return 'non_bsl_code must be empty for category codes 1, 2, 3, 4, 5, 7'
    if row['category_code'] == 6 and row['non_bsl_code'] not in allowed_values:
        return 'non_bsl_code must be S, L, G, H, F, E, P, N, or R for category code 6'
    return 'Valid'


def bsl_lacks_address_flag_check(row):
    #: convert field to str
    if row['bsl_lacks_address_flag'] not in ('0', '1') and row['category_code'] in (1, 2):
        return 'bsl_lacks_address_flag must have a value of 0 or 1 for category code 1 or 2'
    if row['bsl_lacks_address_flag'] and row['category_code'] in (3, 4, 5, 6, 7):
        return 'bsl_lacks_address_flag must be empty for category codes 3-7'

    return 'Valid'


def latitude_check(row, min_lat=36.8, max_lat=42.2):
    #: Needs to come in as str to maintain precision check (casting float to str will lose any trailing 0s)
    if row['latitude'] and row['category_code'] in (2, 3, 4, 6, 7):
        return 'latitude must be empty for category codes 2, 3, 4, 6, 7'
    if not row['latitude'] and row['category_code'] in (1, 5):
        return 'latitude required for category codes 1 and 5'

    if row['latitude'] and row['category_code'] in (1, 5):
        if not min_lat < float(row['latitude']) < max_lat:
            return f'latitude out of range {min_lat} to {max_lat}'
        if not re.search(r'(?<=\.)[0-9]{6,}', row['latitude']):
            return 'latitude must have a minimum precision of 6 decimal places'
    return 'Valid'


def longitude_check(row, min_long=-114.3, max_long=-109):
    #: Needs to come in as str to maintain precision check (casting float to str will lose any trailing 0s)
    if row['longitude'] and row['category_code'] in (2, 3, 4, 6, 7):
        return 'longitude must be empty for category codes 2, 3, 4, 6, 7'
    if not row['longitude'] and row['category_code'] in (1, 5):
        return 'longitude required for category codes 1 and 5'

    if row['longitude'] and row['category_code'] in (1, 5):
        if not min_long < float(row['longitude']) < max_long:
            return f'longitude out of range {min_long} to {max_long}'
        if not re.search(r'(?<=\.)[0-9]{6,}', row['longitude']):
            return 'longitude must have a minimum precision of 6 decimal places'
    return 'Valid'

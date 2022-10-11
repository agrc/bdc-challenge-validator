# UGRC BDC Validator

![Build Status](https://github.com/agrc/bdc-challenge-validator/workflows/Build%20and%20Test/badge.svg)
[![codecov](https://codecov.io/gh/agrc/bdc-challenge-validator/branch/main/graph/badge.svg)](https://codecov.io/gh/agrc/bdc-challenge-validator)

A program for validating files prior to submission to the FCC's bulk data challenge portal. It makes sure the proper fields are populated or left blank and that certain fields are formatted correctly based on the FCC's [Bulk Fabric Challenge Data Matrix](https://help.bdc.fcc.gov/hc/en-us/articles/8103937932443-Bulk-Fabric-Challenge-Data-Matrix) and [formatting guide](https://help.bdc.fcc.gov/hc/en-us/articles/8103890293275-How-to-Format-a-Bulk-Fabric-Challenge) as of September 2022.

Requires ArcGIS Pro (unless you're familiar with conda environments).

Note: It does not check the name, email, and phone number columns but assumes these are correct or easy to validate manually.

## Installation

1. Open the command prompt installed alongside ArcGIS Pro
   - Start > ArcGIS > Python Command Prompt
   - There may be other similarly named entries; make sure to use this one. You should get a command line that starts with `(arcgispro-py3) c:\...>`
1. Type the following to install the script from the Python Package Index (pypi.org):
   - `pip install ugrc-bdc-challenge-validator`

## Usage

1. If it's not already open from the installation, launch the Python Command Prompt
   - Start > ArcGIS > Python Command Prompt
1. Use the `cd` command to change the current directory to the folder where you've got your csv file
   - For example, `cd c:\gis\projects\broadband_fabric`.
   - The command line prompt should change to this directory, like so: `(arcgispro-py3) c:\gis\projects\broadband_fabric>`
   - If any of the folders in this path have a space in their name, you'll need to surround the whole path with quotes: `cd "c:\gis\projects\broadband fabric"`
   - You can hit `tab` after typing the first few letters of each folder name and it will try to autocomplete the name for you. This only works if the letters you've already typed are enough to uniquely identify the folder. For example, if I've got the folders `Projects` and `Presentations`, I'd have to type `Pro` before hitting tab for it to autocomplete `Projects`.
      - If there are multiple folders with the same starting letters, you can type those and hit `tab` twice to see all the options.
      - Autocomplete will automatically add the quotation marks if the full name has a space in it (so long as the space isn't needed to uniquely identify the name for the autocomplete).
1. Type `bdcvalidator` followed by the name of the csv file in the current directory you want to test:
   - `bdcvalidator challenge.csv`
1. The validator will run it's checks. You should see progress messages printed out, and if errors were found it will write a new csv with `_validator_results` appended to the end of the filename in the same directory
   - ie, `challenge_validator_results.csv`
   - This file will be overwritten everytime you run the validator. If you want to save it before running it again, rename it to something else.
1. Open the resulting CSV in a spreadsheet program and sort on the various `_result` columns to find the problem rows for each column.

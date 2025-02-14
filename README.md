# README

## Overview
A tool to calculate weighted averages and sums of LPJ-GUESS variables for NUTS-areas and on a country-level.

It takes LPJ-GUESS sample data and NUTS-area shapefile as inputs, and outputs csv files containing yearly averages and sums for each NUTS-area and country.

## Requirements
Tested with Python version 3.12.2

The following Python libraries are used: geopandas, pandas, shapely

Installing instructions in bash:

```bash
pip install geopandas pandas shapely
```

## Usage
You can clone the repository with the following command:

```bash
git clone https://github.com/joelPuronaho/forest_data_aggregation.git
```


Then, navigate to /src/ inside the repository and run (bash):
```bash
python LPJ-GUESS_averages_sums.py
```

Or use any other method you prefer to run the main file.

## Input files
### Shapefiles
- Contains spatial boundary data for NUTS areas e.g.: NUTS_RG_01M_2024_3035.shp where:
    - 2024 = year
    - 3035 = EPSG system
### .out files
- LPJ-GUESS sample outputs

NUTS-data source:
https://gisco-services.ec.europa.eu/distribution/v2/
- Navigate to: NUTS -> ZIPPED FILES -> Choose the preferred scale and file format

## Output files
Outputs are in:
-  /output/csv/ (separator=",", decimal=".")
- /output/excel/ (separator=";", decimal=",")

- Change LPJ-GUESS input data by changing the 'INPUT_FILE_NAME' in 'LPJ-GUESS_averages_sums.py' (e.g. cpool -> diamstruct_cmass_froot_forest)
- Change NUTS-data by changing 'shapefile_path' in LPJ-GUESS_averages_sums.py

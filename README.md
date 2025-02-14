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

## Script Usage
Navigate to /src/, and run (bash):
```bash
python LPJ-GUESS_averages_sums.py
```

## Input files
### Shapefiles
- Contains spatial boundary data for NUTS areas e.g.: NUTS_RG_01M_2024_3035.shp where:
    - 2024 = year
    - 3035 = EPSG system
### .out files
- LPJ-GUESS sample outputs

## Output files
Outputs are in:
-  /output/csv/ (separator=",", decimal=".")
- /output/excel/ (separator=";", decimal=",")

- Change LPJ-GUESS input data by changing the 'INPUT_FILE_NAME' in 'LPJ-GUESS_averages_sums.py' (e.g. cpool -> diamstruct_cmass_froot_forest)
- Change NUTS-data by changing 'shapefile_path' in LPJ-GUESS_averages_sums.py


## Bugs, future changes etc. "selfnotes"

- The method to calculate grid cell and intersection areas is subject to change, if a better, more accurate method is found.
- Country level calculations are currently done based on the grid cell aggregated data. This might create some bias and skew the results -> Solve by creating new script that calculates the greater than NUTS-level data straight from cordinate data without grid cell aggregation 
- Some complicated shapes within grid cells might cause inaccuracies (tested with NUTS-area surface area calculation, complicated NUTS-area shapes resulted in wrong surface areas) -> Solve by checking the grid cell areas and intersection areas

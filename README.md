# README

## Overview
This script calculates weighted averages and sums of LPJ-GUESS variables. They are aggregated for NUTS-areas and on country level . It utilizes GeoPandas for handling geographic data, Pandas for data manipulation, and Shapely for creating geometries. The script is designed to work with shapefiles and CSV files containing spatial information.

## Requirements

Tested with Python version 3.12.2

The following Python libraries are used: geopandas, pandas, shapely

Installing instructions in bash:

```bash
pip install geopandas pandas shapely
```

## Script Usage
1. Navigate to /src/, and in terminal (bash) run: ```python LPJ-GUESS_averages_sums.py```
2. Outputs are in /output/csv/ (separator=",", decimal=".") and /output/excel/ (separator=";", decimal=",")

- Change LPJ-GUESS data by changing the INPUT_FILE_NAME accordingly (e.g. cpool -> diamstruct_cmass_froot_forest) in LPJ-GUESS_averages_sums.py
- Change NUTS-data by changing shapefile_path in LPJ-GUESS_averages_sums.py

## Input files
### Shapefiles
- Contains spatial boundary data for NUTS areas e.g.: NUTS_RG_01M_2024_3035.shp where:
    - 2024 = year
    - 3035 = EPSG system
### .out files
- LPJ-GUESS sample outputs

### Bugs, future changes etc. "selfnotes"
- Country level calculations are currently done based on the grid cell aggregated data. This might create some bias and skew the results -> Solve by creating new script that calculates the greater than NUTS-level data straight from cordinate data without grid cell aggregation 
- Some complicated shapes within grid cells might cause inaccuracies (tested with NUTS-area surface area calculation, complicated NUTS-area shapes resulted in wrong surface areas) -> Solve by checking the grid cell areas and intersection areas

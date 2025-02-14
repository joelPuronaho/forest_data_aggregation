# README

## Overview
A tool to calculate weighted averages and sums of LPJ-GUESS variables for NUTS-areas and on a country-level.

It takes LPJ-GUESS sample data and NUTS-area shapefile as inputs. The outputs are csv files containing yearly averages and sums for each NUTS-area and country.

A grid cell is created for each coordinate in the LPJ-GUESS data. Then a weight is calculated for each data point based on the portion of the grid cell that intersects with a NUTS-area. The weights are then applied for each LPJ-GUESS variable value which are used to calculate the yearly weighted averages and sums.

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


## Possible bugs, future changes etc. "selfnotes"
- The method to calculate grid cell and intersection surface areas is subject to change, if a better more accurate method is found.
- Country level calculations are currently done based on the grid cell aggregated data. This might create some bias and skew the results -> Additional script that calculates the averages straight from the coordinate data without grid cell aggregation in between 
- Some complicated shapes within grid cells might cause inaccuracies (tested with NUTS-area surface area calculation: complicated NUTS-area shapes resulted in inaccurate surface areas) -> Needs to be verified
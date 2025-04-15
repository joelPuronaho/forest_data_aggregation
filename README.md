# README

## Overview
A tool to calculate weighted averages and sums of LPJ-GUESS variables for NUTS-areas and on a country-level.

The code takes LPJ-GUESS sample data and NUTS-area shapefile as inputs. The outputs are csv files containing yearly weighted averages and sums for each NUTS-area and country.

A grid cell is created for each coordinate in the LPJ-GUESS data. Then a weight is calculated for each data-point based on the portion of the grid cell that intersects with given NUTS-area. The weights are then applied for each LPJ-GUESS variable value, which are then used to calculate the yearly weighted averages and sums.

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
python LPJ-GUESS_aggregation.py
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

## src/calculate_grid_cell_surface_areas.py

This script creates grid cells based on the inpu data (LPJ-GUESS sample: cpool.out), and calculates the area of each grid cell with "grid_cells.geometry.area".

It contains identical code to main script "LPJ-GUESS_aggregation.py", all the unnecessary code has been commented for it to be easier to find the relevant parts.

More info on the area calculation function: https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.area.html

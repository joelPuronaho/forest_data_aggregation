# Imports
import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

# Helpers
import convert_and_load_data
import calculate_weighted_sums
import calculate_weighted_averages

#region Create geometry for each coordinate pair. Works with any spatial resolution (degree = coordinate spacing)
def create_geometry(data, lon_column, lat_column, degree):

    # Calculate corner-points of the grid cell from the center coordinate pair
    data['geometry'] = [
        Polygon([(lon - degree / 2, lat - degree / 2), (lon - degree / 2, lat + degree / 2),
                 (lon + degree / 2, lat + degree / 2), (lon + degree / 2, lat - degree / 2)])
        for lon, lat in zip(data[lon_column], data[lat_column])
    ]
    return data
#endregion

#region calculate_grid_cell_and_intersected_area
def calculate_grid_cell_and_intersected_area(forest_data, nuts_areas):

    # Add geometry column of gridd cells to forest_data (0.5-degree resolution cell grid)
    forest_data = create_geometry(forest_data, 'Lon', 'Lat', degree=0.5)

    # Create the GeoDataFrame with CRS EPSG:4326
    grid_cells = gpd.GeoDataFrame(forest_data, geometry=forest_data["geometry"], crs="EPSG:4326")
    
    # Update the EPSG to meters
    grid_cells = grid_cells.to_crs("EPSG:3035")
    
    # Calculating the grid cell areas in km2
    grid_cells['area_km2'] = pd.to_numeric(grid_cells.geometry.area / 1000000, errors='coerce')

    # Set the same EPSG for NUTS-areas
    nuts_areas = nuts_areas.to_crs("EPSG:3035")
    
    # Spatial intersections of grid cells and nuts_areas - the overlapping area of grid cells with NUTS-areas
    intersections = gpd.overlay(grid_cells, nuts_areas, how='intersection')

    # Calculate the intersected area for each grid cell
    intersections['intersection_area_km2'] = pd.to_numeric(intersections['geometry'].area / 1000000, errors='coerce')

    # Ensure 'intersection_weight' is numeric
    intersections['intersection_weight'] = intersections.apply(
        lambda row: pd.to_numeric(row['intersection_area_km2'] / row['area_km2'], errors='coerce'), axis=1
    )

    # Check that all intersection weights are between 0 and 1
    tolerance = 1e-10
    if not all(0 - tolerance <= w <= 1 + tolerance for w in intersections['intersection_weight']):
        raise ValueError("Some weights are outside the expected range of [0, 1].")

    print("5: Grid cells created and intersected areas calculated for grid cells")
    return intersections
#endregion

#region Save results
def save_results(weighted_avg_df, output_path, output_path_semicolon):

    # Save the data to CSV
    weighted_avg_df.to_csv(output_path, index=False)
    print(f"** Weighted averages saved to {output_path}, AND...  **")

    # Save the data to a semicolon-separated file with commas as decimal points (easily workable in excel)
    weighted_avg_df.to_csv(output_path_semicolon, index=False, sep=";", decimal=",")
    print(f"** ...weighted averages saved to {output_path_semicolon} **")
#endregion

#region Extract variable names from input file
# Returns a list of column names except for Lon, Lat, and Year (= variables from LPJ input file)
def extract_variables(forest_data):
    print("4: Variables filtered from forest data columns")
    return [col for col in forest_data.columns if col not in ["Lon", "Lat", "Year"]]
#endregion

#region Input and output data paths

# Shapefile for NUTS-areas
#shapefile_path = '../input_data/nuts_data/NUTS_RG_20M_2021_4326_LEVL_2.shp'
shapefile_path = '../input_data/nuts_data/NUTS_RG_20M_2024_3035_LEVL_2.shp'

# Define input file prefix
INPUT_FILE_NAME = 'cpool'

# File extensions for .out and .csv
forest_data_path_out = '../input_data/lpj-guess_out/' + INPUT_FILE_NAME + '.out'
forest_data_path_csv = '../output/lpj-guess_csv/' + INPUT_FILE_NAME + '.csv'

# Define output file paths - *Note: "semicolon" paths are for easy access in excel* 
output_path_nuts_avg = '../output/csv/nuts_weighted_averages_' + INPUT_FILE_NAME + '.csv'
output_path_semicolon_nuts_avg = '../output/excel/nuts_weighted_averages_' + INPUT_FILE_NAME + '_excel.csv'

output_path_country_avg = '../output/csv/country_weighted_avgs_' + INPUT_FILE_NAME + '.csv'
output_path_semicolon_country_avg = '../output/excel/country_weighted_avgs_' + INPUT_FILE_NAME + '_excel.csv'

output_path_sum = '../output/csv/nuts_weighted_sums_' + INPUT_FILE_NAME + '.csv'
output_path_semicolon_sum = '../output/excel/nuts_weighted_sums_' + INPUT_FILE_NAME + '_excel.csv'

output_path_country_sum = '../output/csv/country_weighted_sums_' + INPUT_FILE_NAME + '.csv'
output_path_semicolon_country_sum = '../output/excel/country_weighted_sums_' + INPUT_FILE_NAME + '_excel.csv'
#endregion

def main():
    if not os.path.exists(forest_data_path_out) or not os.path.exists(shapefile_path):
        print("Input files not found. Check the file paths.")
        return
    
    convert_and_load_data.convert_out_file_to_csv(forest_data_path_out, forest_data_path_csv)

    nuts_areas = convert_and_load_data.load_data_shp(shapefile_path)
    forest_data = convert_and_load_data.load_data_csv(forest_data_path_csv)

    # Extract the variables from the LPJ-GUESS input file
    variables_to_include = extract_variables(forest_data)

    # Create grid cell, calculate intersected areas for NUTS-areas and grid cells
    intersections = calculate_grid_cell_and_intersected_area(forest_data, nuts_areas)

    # Calculate weighted averages: NUTS-area level
    weighted_avg_df_nuts = calculate_weighted_averages.calculate_weighted_averages_nuts_level(intersections, variables_to_include)
    save_results(weighted_avg_df_nuts, output_path_nuts_avg, output_path_semicolon_nuts_avg)

    # Calculate weighted averages: Country level
    weighted_avg_df_country = calculate_weighted_averages.calculate_weighted_averages_country_level(intersections, variables_to_include)
    save_results(weighted_avg_df_country, output_path_country_avg, output_path_semicolon_country_avg)

    # Calculate weighted sums: NUTS-area level
    weighted_sum_df = calculate_weighted_sums.calculate_weighted_sums_nuts_level(intersections, variables_to_include)
    save_results(weighted_sum_df, output_path_sum, output_path_semicolon_sum)

    # Calculate weighted sums: Country level
    weighted_sum_df = calculate_weighted_sums.calculate_weighted_sums_country_level(intersections, variables_to_include)
    save_results(weighted_sum_df, output_path_country_sum, output_path_semicolon_country_sum)

if __name__ == "__main__":
    main()

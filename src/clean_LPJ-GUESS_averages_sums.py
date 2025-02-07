import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import convert_and_load_data
import weighted_sum

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

    # Create the GeoDataFrame with CRS EPSG:3035 (projected CRS)
    # - EPSG:3035 suitable for area calculations in europe (in meters)

    # ** Note ** 
    # - For some reason, if the next line has crs="EPSG:4326", the calculation does not work. So first set the data to EPSG:4326, then on the next line to EPSG:3035.
    #   - Setting EPSG:3035 on the next line, the dataframe has still the geometry as degrees
    #   - Setting EPSG:4326 on the next line, and then "grid_cells = grid_cells.to_crs("EPSG:3035")" the geometry updates to meters
    #       -> "gpd.GeoDataFrame" does not update the EPSG correctly -> need to update it after initial loading of data
    # ** Note ** 

    grid_cells = gpd.GeoDataFrame(forest_data, geometry=forest_data["geometry"], crs="EPSG:4326")

    # Calculating the grid cell area: "".geometry.area"
    
    # ** Note **
    # - Here, the method can be changed if necessary
    # - For grid cells, this is accurate. For NUTS-areas, there are issues with some areas
    # ** Note **

    grid_cells = grid_cells.to_crs("EPSG:3035")             # **Necessary** for correct area calculations with xxx.geometry.area
    
    grid_cells['area_km2'] = grid_cells.geometry.area / 1000000
    grid_cells.to_csv("grid_cells", index=False, sep=";", decimal=",")

    # Set the same EPSG for NUTS-areas
    nuts_areas = nuts_areas.to_crs("EPSG:3035")             # **Necessary**
    
    # Spatial intersections of grid cells and nuts_areas - the overlapping area of grid cells with NUTS-areas
    intersections = gpd.overlay(grid_cells, nuts_areas, how='intersection')
    
    # Calculate the area of grid cell overlapping with NUTS-area 
    intersections['intersection_area_km2'] = intersections['geometry'].area / 1000000

    # Calculate the weights per grid cell in km^2
    intersections['intersection_weight'] = intersections.apply(
        lambda row: row['intersection_area_km2'] / row['area_km2'], axis=1
    )

    print("5: Grid cells created and intersected areas calculated for grid cells")
    return intersections
#endregion

#region Calculate weighted averages per NUTS-area
def calculate_weighted_averages_nuts_level(intersections, variables_to_include):
    
    # Set up a list to store resulting dataframes for each variable
    results = []

    for variable in variables_to_include:
        
        # Calculate the weighted values for each variable, handle NULL data (NULL -> NaN)
        intersections['weighted_value'] = pd.to_numeric(intersections[variable], errors='coerce') * intersections['intersection_weight']
        weighted_avg_series = intersections.groupby(['NUTS_ID', 'Year'], as_index=False, group_keys=False).apply(
            lambda group: pd.Series({
                f'weighted_avg_{variable}': group['weighted_value'].sum() / group['intersection_weight'].sum()
            }),
            include_groups=False
        )
        # Merge the data
        results.append(weighted_avg_series)

    # Print progress
    print("6: Weighted averages calculated per NUTS-area")

    # Return results: filter duplicate columns from output
    return pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]

#endregion

#region Calculate weighted averages per country
def calculate_weighted_averages_country_level(intersections, variables_to_include):

    # Set up a list to store resulting dataframes for each variable
    results = []
    
    for variable in variables_to_include:
        # Calculate the weighted values for each variable
        intersections['weighted_value'] = pd.to_numeric(intersections[variable], errors='coerce') * intersections['intersection_weight']
        intersections['Country'] = intersections['NUTS_ID'].str[:2]  # Extract the first two characters to identify each country
        
        weighted_avg_series = intersections.groupby(['Country', 'Year'], as_index=False, group_keys=False).apply(
            lambda group: pd.Series({
                f'weighted_avg_{variable}': group['weighted_value'].sum() / group['intersection_weight'].sum()
            }),
            include_groups=False
        )
        # Merge the data
        results.append(weighted_avg_series)
    
    # Print progress
    print("7: Weighted averages calculated per country")

    # Return results: filter duplicate columns from output
    return pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]
#endregion

#region Save results
def save_results(weighted_avg_df, output_path, output_path_semicolon):

    # Save the data to CSV
    weighted_avg_df.to_csv(output_path, index=False)
    
    # Save the data to a semicolon-separated file with commas as decimal points (easily workable in excel)
    weighted_avg_df.to_csv(output_path_semicolon, index=False, sep=";", decimal=",")
    print(f"** Weighted averages saved to {output_path}, AND...  **")
    print(f"** ...weighted averages saved to {output_path_semicolon} **")
#endregion


#region Input and output data paths
# Shapefile for NUTS-areas
#shapefile_path = '../input_data/nuts_data/NUTS_RG_20M_2021_4326_LEVL_2.shp'
shapefile_path = '../input_data/nuts_data/NUTS_RG_20M_2024_3035_LEVL_2.shp'

# Define input file prefix
INPUT_FILE_NAME = 'cpool'
#INPUT_FILE_NAME = 'cpool_2020' # Simplified output for 'Total' and year 2020 only

# File extensions for .out and .csv
forest_data_path_out = '../input_data/lpj-guess_out/' + INPUT_FILE_NAME + '.out'
forest_data_path_csv = '../output/lpj-guess_csv/' + INPUT_FILE_NAME + '.csv'

# Define output file paths - *semicolon* paths are for easy access in excel 
output_path_nuts_avg = '../output/weighted_averages_cpool_out.csv'
output_path_semicolon_nuts_avg = '../output/weighted_averages_cpool_out_excel.csv'

output_path_country_avg = '../output/country_weighted_avgs_cpool_out.csv'
output_path_semicolon_country_avg = '../output/country_weighted_avgs_cpool_out_excel.csv'

output_path_sum = '../output/weighted_sums_cpool_out.csv'
output_path_semicolon_sum = '../output/weighted_sums_cpool_out_excel.csv'
#endregion


# Returns a list of column names except for Lon, Lat, and Year (=variables)
def extract_variables(forest_data):
    print("4: Variables filtered from forest data columns")
    return [col for col in forest_data.columns if col not in ["Lon", "Lat", "Year"]]

def main():
    if not os.path.exists(forest_data_path_out) or not os.path.exists(shapefile_path):
        print("Input files not found. Please check the paths.")
        return
    
    convert_and_load_data.convert_out_file_to_csv(forest_data_path_out, forest_data_path_csv)

    nuts_areas = convert_and_load_data.load_data_shp(shapefile_path)
    forest_data = convert_and_load_data.load_data_csv(forest_data_path_csv)

    # Extract the variables in the LPJ-GUESS input file
    variables_to_include = extract_variables(forest_data)

    # Create grid cell, calculate intersected areas for NUTS-areas and grid cells
    intersections = calculate_grid_cell_and_intersected_area(forest_data, nuts_areas)

    # Calculate weighted averages: NUTS-area level
    weighted_avg_df_nuts = calculate_weighted_averages_nuts_level(intersections, variables_to_include)
    save_results(weighted_avg_df_nuts, output_path_nuts_avg, output_path_semicolon_nuts_avg)

    # Calculate weighted averages: Country level
    weighted_avg_df_country = calculate_weighted_averages_country_level(intersections, variables_to_include)
    save_results(weighted_avg_df_country, output_path_country_avg, output_path_semicolon_country_avg)

    # Calculate weighted sums: NUTS-area level
    weighted_sum_df = weighted_sum.calculate_weighted_sums_nuts_level(intersections, variables_to_include)
    save_results(weighted_sum_df, output_path_sum, output_path_semicolon_sum)

if __name__ == "__main__":
    main()

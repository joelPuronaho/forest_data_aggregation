import csv
import geopandas as gpd
import pandas as pd

#region Convert out to csv 
# *Selfnote: This could be removed and use .out files for the calculations
def convert_out_file_to_csv(input_file, output_file):
    
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Extract the header and data
    header = lines[0].strip().split()
    data = [line.strip().split() for line in lines[1:]]

    # Write header and data to a CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)
    print(f"1: .out file {input_file} transformed to {output_file}")
#endregion

#region Load data for LPJ-GUESS and NUTS-areas
def load_data_shp(shapefile_path):

    # Save NUTS-area data
    try:
        nuts_areas = gpd.read_file(shapefile_path)
        print(f"2: Shapefile '{shapefile_path}' loaded into 'nuts_areas'")
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        exit(1)
    return nuts_areas
#endregion

#region Load data for LPJ-GUESS and NUTS-areas
def load_data_csv(forest_data_path_csv):
    
    # Save forest data
    try:
        forest_data = pd.read_csv(forest_data_path_csv)
        print(f"3: Forest data csv '{forest_data_path_csv}' loaded into 'forest_data'")
    except FileNotFoundError:
        print(f"Error: File {forest_data_path_csv} not found.")
        exit(1)
    return forest_data
#endregion
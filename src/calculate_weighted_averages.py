import pandas as pd

#region Calculate weighted averages per NUTS-area
def calculate_weighted_averages_nuts_level(intersections, variables_to_include):
    
    # Set up a list to store resulting dataframes for each variable
    results = []

    for variable in variables_to_include:
        # Calculate the weighted values for each variable
        intersections['weighted_value'] = pd.to_numeric(intersections[variable], errors='coerce') * intersections['intersection_weight']

        # Calculate the weighted averages for a variable for each year
        weighted_avg_series = intersections.groupby(['NUTS_ID', 'Year'], as_index=False, group_keys=False).apply(
            lambda group: pd.Series({
                f'weighted_avg_{variable}': group['weighted_value'].sum() / group['intersection_weight'].sum()
            }),
            include_groups=False
        )
        # Merge the data
        results.append(weighted_avg_series)

    # Print progress
    print("6: Weighted averages calculated per NUTS area")

    # Filter duplicate columns from the output and return results 
    results = pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]
    return results
#endregion

#region Calculate weighted averages per country
def calculate_weighted_averages_country_level(intersections, variables_to_include):

    # Set up a list to store resulting dataframes for each variable
    results = []
    
    for variable in variables_to_include:
        # Calculate the weighted values for each variable
        intersections['weighted_value'] = pd.to_numeric(intersections[variable], errors='coerce') * intersections['intersection_weight']

        # Extract the first two characters to identify each country
        intersections['Country'] = intersections['NUTS_ID'].str[:2]

        # Calculate the weighted averages for a variable for each year
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

    # Filter duplicate columns from the output and return results 
    results = pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]
    return results
#endregion

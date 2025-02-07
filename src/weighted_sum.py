import pandas as pd

#region Calculate weighted sums per country
def calculate_weighted_sums_country_level(intersections, variables_to_include):

    # Set up a list to store resulting dataframes for each variable
    results = []
    
    for variable in variables_to_include:
        # Calculate the weighted values for each variable
        intersections['weighted_value'] = pd.to_numeric(intersections[variable], errors='coerce') * intersections['intersection_weight']
        # Extract the first two characters to identify each country
        intersections['Country'] = intersections['NUTS_ID'].str[:2]
        
        weighted_sum_series = intersections.groupby(['Country', 'Year'], as_index=False, group_keys=False).apply(
            lambda group: pd.Series({
                f'weighted_avg_{variable}': group['weighted_value'].sum()
            }),
            include_groups=False
        )
        
        # Merge the data
        results.append(weighted_sum_series)

    # Print progress
    print("9: Weighted sums calculated per country")

    # Return results: filter duplicate columns from output
    return pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]
#endregion

#region Calculate weighted sum per NUTS-area
def calculate_weighted_sums_nuts_level(intersections, variables_to_include):

    # Set up a list to store resulting dataframes for each variable
    results = []
    
    for variable in variables_to_include:
        # Calculate the weighted values for each variable
        intersections['weighted_value'] = pd.to_numeric(intersections[variable], errors='coerce') * intersections['intersection_weight']
        
        # Calculate the weighted averages for each NUTS-area for each year
        weighted_sum_series = intersections.groupby(['NUTS_ID', 'Year'], as_index=False, group_keys=False).apply(
            lambda group: pd.Series({
                f'weighted_sum_{variable}': group['weighted_value'].sum()
            }),
            include_groups=False
        )
        # Merge the data
        results.append(weighted_sum_series)
    
    # Print progress
    print("8: Weighted sums calculated per NUTS-area")

    # Return results: filter duplicate columns from output
    return pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]
#endregion
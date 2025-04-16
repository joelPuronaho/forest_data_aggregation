import pandas as pd
from io import StringIO

# Your input data
data = "../../input_data/filtered_nuts2_surface_areas_landuse_total.csv"

# Read data into a DataFrame
df = pd.read_csv(data, sep=';')
print(df)

# Extract country code (first two letters of NUTS_ID)
df['country_code'] = df['NUTS_ID'].str[:2]

# Group by country and sum surface area
country_df = df.groupby('country_code', as_index=False).agg({
    'official_surface_area_2021': 'sum'
})

# Add remaining constant columns
country_df['freq'] = 'A'
country_df['landuse'] = 'TOTAL'
country_df['unit'] = 'KM2'

# Rename column to match format
country_df.rename(columns={'country_code': 'NUTS_ID'}, inplace=True)

# Save to CSV
country_df.to_csv('../../input_data/country_level_filtered_nuts2_surface_areas_landuse_total.csv', sep=';', index=False)

print(country_df)

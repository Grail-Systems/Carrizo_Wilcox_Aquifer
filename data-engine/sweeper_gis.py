import geopandas as gpd
import os

print("Spinning up the Grail Systems Data Engine...")

input_shapefile = "raw-data/NEW_major_aquifers_dd.shp" 
output_geojson = "frontend/wilcox_aquifer.json"

try:
    print(f"Loading heavy shapefile from {input_shapefile}...")
    gdf = gpd.read_file(input_shapefile)
    
    # Target locked onto the exact TWDB spelling
    print("Scanning for CARRIZO boundaries...")
    wilcox_gdf = gdf[gdf['AQ_NAME'].str.contains("CARRIZO", case=False, na=False)]
    
    if wilcox_gdf.empty:
        print("\nERROR: Could not find 'CARRIZO'.")
    else:
        print("Target acquired! Crunching coordinates for 3D web projection...")
        wilcox_gdf = wilcox_gdf.to_crs(epsg=4326)
        
        wilcox_gdf.to_file(output_geojson, driver="GeoJSON")
        print(f"\nSuccess! 3D blueprint deployed to {output_geojson}")

except Exception as e:
    print(f"System Error: {e}")

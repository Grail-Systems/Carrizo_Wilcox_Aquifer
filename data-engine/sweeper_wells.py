import geopandas as gpd

print("Spinning up the Grail Systems Data Engine...")
wells_shapefile = "raw-data/TWDB_Groundwater.shp"
output_geojson = "frontend/threat_wells.json"

try:
    print("Loading database...")
    wells_gdf = gpd.read_file(wells_shapefile)
    
    # 1. Lock onto the Aquifer
    cw_wells = wells_gdf[wells_gdf['AquiferCod'].str.contains("CRWX|WILCOX|CARRIZO|124", case=False, na=False)]
    
    # 2. Filter only the massive industrial/municipal straws
    threat_categories = ['Industrial', 'Industrial (cooling)', 'Power', 'Public Supply', 'Fracking Supply', 'Bottling']
    threat_wells = cw_wells[cw_wells['PrimaryWat'].isin(threat_categories)]
    
    print(f"Target Acquired: Isolated {len(threat_wells)} High-Volume Threat Wells.")
    print("Crunching coordinates and deploying to defense grid...")
    
    # 3. Project to standard web GPS format and export
    threat_wells = threat_wells.to_crs(epsg=4326)
    threat_wells.to_file(output_geojson, driver="GeoJSON")
    
    print(f"Success! Targets locked and exported to {output_geojson}")

except Exception as e:
    print(f"System Error: {e}")

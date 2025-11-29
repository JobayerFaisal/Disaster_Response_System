from dashboard.db import get_conn  # Import the get_conn function
import geopandas as gpd
import pandas as pd
import shapely.wkb as wkb
import streamlit as st

st.title("🛰 Interactive Map View")

# Get the SQLAlchemy engine
conn = get_conn()

# Query the database to get the spatial data
df = pd.read_sql("""
    SELECT 
        name,
        ST_AsBinary(center) AS geom,
        radius_km,
        risk_level
    FROM sentinel_zones
""", conn)

# No need to explicitly close the connection as SQLAlchemy handles that

# Use GeoPandas' from_wkb to directly convert the WKB bytes into geometries
df["geometry"] = gpd.GeoSeries.from_wkb(df["geom"])

# Convert the dataframe to a GeoDataFrame for mapping
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# Display the map in Streamlit
st.map(gdf)

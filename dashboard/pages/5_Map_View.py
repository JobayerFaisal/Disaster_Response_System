import streamlit as st
from dashboard.db import get_conn
import geopandas as gpd
import pandas as pd
import shapely.wkb as wkb

st.title("🛰 Interactive Map View")

conn = get_conn()
df = pd.read_sql("""
    SELECT 
        name,
        ST_AsBinary(center) AS geom,
        radius_km,
        risk_level
    FROM sentinel_zones
""", conn)

conn.close()

df["geometry"] = df["geom"].apply(lambda x: wkb.loads(bytes(x)))
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

st.map(gdf)

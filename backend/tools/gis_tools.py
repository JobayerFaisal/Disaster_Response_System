# placeholder
import json
from shapely.geometry import Polygon, mapping, Point
import random


def generate_flood_geojson():
    """
    Generates a simple flood polygon set for the map.
    In production, this will come from DEM/rainfall models or PostGIS.
    """

    # Example polygons
    zones = [
        {
            "area": "North Zone",
            "risk": "RED",
            "depth_m": round(random.uniform(1.0, 2.5), 2),
            "polygon": [
                [90.412, 23.812], [90.414, 23.812],
                [90.414, 23.815], [90.412, 23.815], [90.412, 23.812]
            ]
        },
        {
            "area": "South Zone",
            "risk": "YELLOW",
            "depth_m": round(random.uniform(0.3, 1.0), 2),
            "polygon": [
                [90.408, 23.805], [90.410, 23.805],
                [90.410, 23.808], [90.408, 23.808], [90.408, 23.805]
            ]
        }
    ]

    features = []
    for z in zones:
        poly = Polygon(z["polygon"])
        features.append({
            "type": "Feature",
            "properties": {
                "area": z["area"],
                "risk": z["risk"],
                "depth_m": z["depth_m"]
            },
            "geometry": mapping(poly)
        })

    return {
        "type": "FeatureCollection",
        "features": features
    }


def get_blocked_roads(flood_geojson):
    """
    Marks roads as blocked if they intersect with flood polygons.
    Placeholder: returns mock blocked roads.
    """

    return [
        {"road": "Bridge-1", "status": "BLOCKED"},
        {"road": "Highway-5", "status": "OPEN"}
    ]

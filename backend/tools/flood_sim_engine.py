from shapely.geometry import Polygon, mapping
import random


def compute_flood_spread(weather, river):
    """
    Simplified physical flood simulation:
    - Heavy rainfall = more zones affected
    - River rise rate = deeper water
    - Random variation simulates topographic flow
    """

    intensity = weather["rainfall_mm"]
    rise = river["water_level_m"]

    # Basic severity calc
    severity = (intensity / 100) + (rise / 5)

    zones = []

    if severity > 2.5:
        zones.append(make_zone("North", "RED", round(random.uniform(1.2, 2.4), 2)))
    if severity > 1.2:
        zones.append(make_zone("South", "YELLOW", round(random.uniform(0.5, 1.2), 2)))
    else:
        zones.append(make_zone("East", "GREEN", 0.2))

    geojson = {
        "type": "FeatureCollection",
        "features": [z["feature"] for z in zones]
    }

    return {"zones": zones, "geojson": geojson}


def make_zone(name, risk, depth):
    poly = Polygon([
        [90.41 + random.uniform(-0.01, 0.01), 23.81 + random.uniform(-0.01, 0.01)],
        [90.42 + random.uniform(-0.01, 0.01), 23.81 + random.uniform(-0.01, 0.01)],
        [90.42 + random.uniform(-0.01, 0.01), 23.82 + random.uniform(-0.01, 0.01)],
        [90.41 + random.uniform(-0.01, 0.01), 23.82 + random.uniform(-0.01, 0.01)]
    ])

    return {
        "area": name,
        "risk": risk,
        "depth_m": depth,
        "feature": {
            "type": "Feature",
            "properties": {"risk": risk, "depth_m": depth},
            "geometry": mapping(poly)
        }
    }

# placeholder
def analyze_infrastructure(drone, flood):
    return {
        "hospitals": {
            "capacity": "70% full",
            "status": "Operational"
        },
        "roads": [
            {"name": "Bridge-1", "status": "CLOSED" if drone["blocked_bridge"] else "OPEN"},
            {"name": "Highway-7", "status": "OPEN"}
        ],
        "power_grid": "Multiple local outages",
        "shelter_updates": [
            {"name": "School #12", "occupancy": "450/600"},
            {"name": "Temple Shelter", "occupancy": "290/300"}
        ]
    }

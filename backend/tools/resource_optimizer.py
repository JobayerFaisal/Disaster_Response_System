# placeholder
def optimize_resources(infra):
    """
    Allocates:
    - rescue boats
    - food packs
    - medical teams
    """

    boats = []
    medical = []
    supplies = []

    if "roads" in infra:
        for r in infra["roads"]:
            if r["status"] == "BLOCKED":
                boats.append({"zone": r["road"], "boats": 2})

    medical.append({"hospital": "Central Hospital", "teams": 3})
    supplies.append({"shelter": "School #12", "food_packs": 500})

    return {
        "boats": boats,
        "medical": medical,
        "supplies": supplies
    }

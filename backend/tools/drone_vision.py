# placeholder
def analyze_drone_image(image_description: str):
    """
    Placeholder for OpenAI Vision.
    This version interprets a textual description.
    """

    if "people" in image_description.lower():
        people = 10
    else:
        people = 0

    blocked = "bridge" in image_description.lower()

    return {
        "people_detected": people,
        "blocked_bridge": blocked,
        "notes": image_description
    }

# placeholder
import logging

logger = logging.getLogger("flood_ai")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

logger.addHandler(handler)

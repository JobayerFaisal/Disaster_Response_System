from fastapi import APIRouter
from backend.api.db import get_pool

router = APIRouter()

@router.get("/")
async def get_predictions(limit: int = 50):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT * FROM flood_predictions
            ORDER BY timestamp DESC
            LIMIT $1
        """, limit)
    await pool.close()
    return [dict(r) for r in rows]

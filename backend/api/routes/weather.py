from fastapi import APIRouter
from backend.api.db import get_pool

router = APIRouter()

@router.get("/latest")
async def latest_weather():
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT * FROM weather_data
            ORDER BY timestamp DESC
            LIMIT 1
        """)
    await pool.close()
    return dict(row) if row else {}

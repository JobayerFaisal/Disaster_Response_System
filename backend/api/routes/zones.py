from fastapi import APIRouter
from backend.api.db import get_pool

router = APIRouter()

@router.get("/")
async def all_zones():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM sentinel_zones")
    await pool.close()
    return [dict(r) for r in rows]

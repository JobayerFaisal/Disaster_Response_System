from fastapi import WebSocket
import asyncio
from backend.api.db import get_pool


async def alerts_ws(websocket: WebSocket):
    await websocket.accept()
    pool = await get_pool()

    try:
        while True:
            async with pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT message, severity, timestamp
                    FROM environmental_alerts
                    ORDER BY timestamp DESC
                    LIMIT 1
                """)
            await websocket.send_json(dict(rows[0]) if rows else {})
            await asyncio.sleep(3)
    except Exception:
        pass
    finally:
        await pool.close()
        await websocket.close()

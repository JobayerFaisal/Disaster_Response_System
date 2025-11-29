# # placeholder
# from fastapi import FastAPI, WebSocket
# from graph.workflow import app
# from graph.state import FloodState
# import json

# api = FastAPI()

# @api.websocket("/stream")
# async def stream(ws: WebSocket):
#     await ws.accept()
#     state = FloodState()

#     async for updated_state in app.astream(state):
#         await ws.send_text(json.dumps(updated_state.dict()))

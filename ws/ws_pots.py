import asyncio
import pydantic
from typing import List, Dict
# from typing_extensions import TypedDict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import sys

sys.path.append("..")
from lib import firebase

from models.Pot import HealthMetricUpdate
from models.utils import validate_model

router = APIRouter()
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str : WebSocket] = {} #TODO: change type to pot id

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket.path_params['pot_id']] = websocket
        print("WS connected with Pot {}".format(websocket.path_params['pot_id']))
        print("Connected WSs: {}".format(self.active_connections.keys()))

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, pot_id: str):
        if pot_id in self.active_connections:
            websocket: WebSocket = self.active_connections[pot_id]
            await websocket.send_text(message)
        else:
            print("Websocket for Pot {} not found".format(pot_id))

    async def broadcast(self, message: str):
        for pot_id in self.active_connections:
            print("Broadcasting to Pot {}".format(pot_id))
            await self.active_connections[pot_id].send_text(message)
            print("Broadcast to Pot {} complete".format(pot_id))

manager = ConnectionManager()

@router.websocket("/ws/{pot_id}")
async def websocket_endpoint(websocket: WebSocket, pot_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            # validate_model(HealthMetricUpdate, data)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{pot_id} says: {data}")
    
    except pydantic.error_wrappers.ValidationError as e:
        print("Invalid data model")
        print(e)           

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{pot_id} left the chat")
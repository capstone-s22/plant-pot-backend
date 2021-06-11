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

    def check_existing_connections(self, prefix_msg="Existing Connections"):
        f = open("wsConnections.txt", "r")
        print(f.read())
        print("{} : {}".format(prefix_msg, self.active_connections.keys()))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        f = open("wsConnections.txt", "a")
        f.write(websocket.path_params['pot_id'])
        f.close()

        self.active_connections[websocket.path_params['pot_id']] = websocket
        print("WS connected with Pot {}".format(websocket.path_params['pot_id']))
        print("Connected WSs: {}".format(self.active_connections.keys()))

    def disconnect(self, pot_id):
        self.check_existing_connections("Before disconnect")
        print(pot_id)
        self.check_existing_connections()
        # self.active_connections.pop(pot_id, None)
        del self.active_connections[pot_id]
        self.check_existing_connections("After disconnect")

    async def send_personal_message(self, message: str, pot_id: str):
        self.check_existing_connections("Before sending message")
        if pot_id in self.active_connections:
            websocket: WebSocket = self.active_connections[pot_id]
            await websocket.send_text(message)
        else:
            print("Websocket for Pot {} not found".format(pot_id))

    async def broadcast(self, message: str):
        self.check_existing_connections("Broadcasting to")
        for pot_id in self.active_connections:
            await self.active_connections[pot_id].send_text(message)
            print("Broadcast to Pot {} complete".format(pot_id))

manager = ConnectionManager()

@router.websocket("/ws/{pot_id}")
async def websocket_endpoint(websocket: WebSocket, pot_id: str):
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
        print("------------------")
        manager.disconnect(pot_id)
import pydantic
from typing import Dict
# from typing_extensions import TypedDict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from validations.schemas import validate_model
from ws.manager import crud_manager

router = APIRouter()
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str : WebSocket] = {} #TODO: change type to pot id

    def check_existing_connections(self, prefix_msg="Existing Connections"):
        print("{} : {}".format(prefix_msg, self.active_connections.keys()))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket.path_params['pot_id']] = websocket
        print("WS connected with Pot {}".format(websocket.path_params['pot_id']))
        print("Connected WSs: {}".format(self.active_connections.keys()))

    def disconnect(self, pot_id):
        self.check_existing_connections("Before disconnect")
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
        if len(self.active_connections) > 0:
            for pot_id in self.active_connections:
                await self.active_connections[pot_id].send_text(message)
                print("Broadcast to Pot {} complete".format(pot_id))
        else:
            print("No websocket connections")

    async def process_message(self, data):
        try:
            message_obj = await validate_model(data)
            response = await crud_manager(message_obj)
            return response
        except Exception as e:
            return e

@router.websocket("/ws/{pot_id}")
async def websocket_endpoint(websocket: WebSocket, pot_id: str):
    # print(manager)
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            response = await manager.process_message(data)
            await manager.send_personal_message(response, pot_id)
            # await manager.broadcast(f"Client #{pot_id} says: {data}")
    
    except pydantic.error_wrappers.ValidationError as e:
        print("Invalid data model")
        print(e)           
        await manager.send_personal_message("Invalid data model", pot_id)

    except WebSocketDisconnect:
        print("------------------")
        manager.disconnect(pot_id)

manager = ConnectionManager()

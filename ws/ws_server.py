import json
import pydantic
from typing import Dict, List
# from typing_extensions import TypedDict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from lib.custom_logger import logger
from validations import be2pot_schemas, pot2be_schemas
from ws.manager import crud_manager

router = APIRouter()
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str : WebSocket] = {} #TODO: change type to pot id

    def check_existing_connections(self, prefix_msg="Existing Connections"):
        logger.info("{} : {}".format(prefix_msg, self.active_connections.keys()))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket.path_params['pot_id']] = websocket
        logger.info("WS connected with Pot {}".format(websocket.path_params['pot_id']))
        logger.info("Connected WSs: {}".format(self.active_connections.keys()))

    def disconnect(self, pot_id):
        self.check_existing_connections("Before disconnect")
        # self.active_connections.pop(pot_id, None)
        del self.active_connections[pot_id]
        self.check_existing_connections("After disconnect")

    async def send_personal_message_text(self, message: str, pot_id: str):
        self.check_existing_connections("Before sending message")
        if pot_id in self.active_connections:
            websocket: WebSocket = self.active_connections[pot_id]
            await websocket.send_text(message)
            # logger.info("Sent Pot {} for message: {}".format(pot_id, message))
            logger.info(json.dumps(message))
        else:
            message["error_msg"] = "Websocket for Pot {} not found".format(pot_id)
            logger.error(json.dumps(message))
    async def send_personal_message_json(self, message: dict, pot_id: str):
        self.check_existing_connections("Before sending message (json)")
        if pot_id in self.active_connections:
            websocket: WebSocket = self.active_connections[pot_id]
            await websocket.send_json(message)
            # logger.info("Sent Pot {} for message: {}".format(pot_id, message))
            logger.info(json.dumps(message))
        else:
            message["error_msg"] = "Websocket for Pot {} not found".format(pot_id)
            logger.error(json.dumps(message))

    async def broadcast(self, message: str):
        self.check_existing_connections("Broadcasting to")
        if len(self.active_connections) > 0:
            for pot_id in self.active_connections:
                await self.active_connections[pot_id].send_text(message)
                # logger.info("Broadcasted to Pot {} for message: {}".format(pot_id, message))
                logger.info(json.dumps(message))
        else:
            message["warning_msg"] = "No websocket connections"
            logger.warning(json.dumps(message))

    async def process_message(self, data):
        try:
            msg_obj: pot2be_schemas.MessageFromPot = await pot2be_schemas.validate_model(data)
            responses: List[be2pot_schemas.MessageToPot] = await crud_manager(msg_obj)
            return responses
        except Exception as e:
            return e

@router.websocket("/ws/{pot_id}")
async def websocket_endpoint(websocket: WebSocket, pot_id: str):
    # print(manager)
    await ws_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            logger.info(json.dumps(data))
            responses: List[be2pot_schemas.MessageToPot] = await ws_manager.process_message(data)
            for response in responses:
                await ws_manager.send_personal_message_json(response.dict(), pot_id)
            # await manager.broadcast(f"Client #{pot_id} says: {data}")
    
    except pydantic.error_wrappers.ValidationError as e:
        print("Invalid data model")
        print(e)           
        await ws_manager.send_personal_message_text("Invalid data model", pot_id)

    except WebSocketDisconnect:
        print("------------------")
        ws_manager.disconnect(pot_id)

ws_manager = ConnectionManager()

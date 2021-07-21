import os
import sys
import pydantic
from typing import Dict, List
# from typing_extensions import TypedDict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from lib.firebase import pots_collection
from lib.custom_logger import logger
from validations import be2pot_schemas, pot2be_schemas
from ws.manager import crud_manager

router = APIRouter()
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str : WebSocket] = {} #TODO: change type to pot id

    def check_existing_connections(self):
        logger.info("Existing Connections - {}".format(list(self.active_connections.keys())))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        pot_id = websocket.path_params['pot_id']
        self.active_connections[pot_id] = websocket
        if pots_collection.document(pot_id).get().exists:
            logger.info("Document {} exists in Firestore".format(pot_id))
            firestore_input = {"connected": True}
            pots_collection.document(pot_id).update(firestore_input)
        else:
            logger.warning("Document {} does not exist in Firestore".format(pot_id))

        logger.info("WS connected with Pot {}".format(pot_id))
        self.check_existing_connections()

    def disconnect(self, pot_id, error_disconnect=False):
        # self.active_connections.pop(pot_id, None)
        del self.active_connections[pot_id]
        if error_disconnect:
            logger.error("Pot {} unexpectedly disconnected".format(pot_id))
        else:
            logger.info("Pot {} gracefully disconnected".format(pot_id))
        self.check_existing_connections()
        if pots_collection.document(pot_id).get().exists:
            firestore_input = {"connected": False}
            pots_collection.document(pot_id).update(firestore_input)

    async def send_personal_message_text(self, message: str, pot_id: str):
        if pot_id in self.active_connections:
            websocket: WebSocket = self.active_connections[pot_id]
            await websocket.send_text(message)
            logger.info(message)
        else:
            message["error_msg"] = "Websocket for Pot {} not found".format(pot_id)
            logger.error(message)
            raise Exception("Websocket for Pot {} not found".format(pot_id)) 

    async def send_personal_message_json(self, message: dict, pot_id: str):
        if pot_id in self.active_connections:
            websocket: WebSocket = self.active_connections[pot_id]
            await websocket.send_json(message)
            logger.info(message)
        else:
            message["error_msg"] = "Websocket for Pot {} not found".format(pot_id)
            logger.error(message)
            raise Exception("Websocket for Pot {} not found".format(pot_id)) 

    async def broadcast(self, message_dict: be2pot_schemas.PotSendDataDictStr):
        if len(self.active_connections) > 0:
            for pot_id in self.active_connections:
                websocket: WebSocket = self.active_connections[pot_id]
                health_check_msg = be2pot_schemas.MessageToPot(
                    action=be2pot_schemas.Action.read,
                    potId=pot_id,
                    data=[be2pot_schemas.PotSendDataDictStr(
                            field=message_dict.field,
                            value=message_dict.value
                            )
                        ]
                )
                await websocket.send_json(health_check_msg.dict())
                logger.info(message_dict)
        else:
            logger.warning("No websocket connections to broadcast to")

    async def process_message(self, data):
        try:
            msg_obj: pot2be_schemas.MessageFromPot = await pot2be_schemas.validate_model(data)
            responses: List[be2pot_schemas.MessageToPot] = await crud_manager(msg_obj)
            return responses
        except Exception as e:
            return e

@router.websocket("/ws/{pot_id}")
async def websocket_endpoint(websocket: WebSocket, pot_id: str):
    await ws_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            logger.info(data)
            responses = await ws_manager.process_message(data)
            for response in responses:
                await ws_manager.send_personal_message_json(response.dict(), pot_id)
            # await manager.broadcast(f"Client #{pot_id} says: {data}")
    
    # TODO: Maybe can remove this 
    except pydantic.error_wrappers.ValidationError as e:
        logger.error(e)           
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_response = be2pot_schemas.MessageToPot(potId=pot_id, 
                                data=[be2pot_schemas.PotSendDataDictStr(
                                    field=be2pot_schemas.PotSendDataStr.error,
                                    value="{}: {}, line {}, {}".format(exc_type, fname, exc_tb.tb_lineno, e))]
                                )

        await ws_manager.send_personal_message_json(err_response.dict(), pot_id)

    except WebSocketDisconnect:
        ws_manager.disconnect(pot_id, error_disconnect=True)
    
    except Exception as e:
        logger.error(e)           
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err_response = be2pot_schemas.MessageToPot(potId=pot_id, 
                                data=[be2pot_schemas.PotSendDataDictStr(
                                    field=be2pot_schemas.PotSendDataStr.error,
                                    value="{}: {}, line {}, {}".format(exc_type, fname, exc_tb.tb_lineno, e))]
                                )

        await ws_manager.send_personal_message_json(err_response.dict(), pot_id)

ws_manager = ConnectionManager()

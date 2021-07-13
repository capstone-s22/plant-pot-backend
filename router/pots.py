import sys
from fastapi import APIRouter
from models.Pot import PotHttpReq
from lib import utils
from lib.pot import new_pot_registration
from lib.firebase import pots_collection

sys.path.append("..")
from ws.ws_server import ws_manager
from lib.custom_logger import logger
router = APIRouter()

@router.get('/health')
async def health():
    try:
        ws_manager.check_existing_connections()
        await ws_manager.broadcast("Broadcast")
        return {"health check": True}
    except Exception as e:
        return f"An Error Occured: {e}"

@router.post('/add')
async def create(new_pot: PotHttpReq):
    try:
        pot_id = new_pot.id
        new_pot = new_pot_registration(pot_id) 
        pots_collection.document(pot_id).set(new_pot.dict())
        logger.warning("New pot added: {}".format(pot_id))
        return {"success": True}
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"
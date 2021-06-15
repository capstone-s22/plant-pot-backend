import sys
from fastapi import APIRouter
from models.Pot import NewPot
from lib import utils
from ws.pot import new_pot_registration
from lib.firebase import pots_collection

sys.path.append("..")
from ws.ws_server import manager
router = APIRouter()

@router.get('/health')
async def create():
    try:
        manager.check_existing_connections()
        await manager.broadcast("Broadcast")
        return {"health check": True}
    except Exception as e:
        return f"An Error Occured: {e}"

@router.post('/add')
async def create(new_pot: NewPot):
    try:
        pot_id = new_pot.id
        data = new_pot_registration(pot_id)
        print(data)
        pots_collection.document(pot_id).set(data)
        return {"success": True}
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"

# @router.put('/update')
# async def update(health_metric_update: HealthMetricUpdate):
#     try:
#         id = health_metric_update.id
#         param_name = health_metric_update.parameter
#         param_value = health_metric_update.value
#         data = utils.update_parameter_schema(param_name,param_value)
#         pots_collection.document(id).update(data)
#         return {"success": True}
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @router.post('/append')
# async def append(health_metric_update: HealthMetricUpdate):
#     try:
#         id = health_metric_update.id
#         param_name = health_metric_update.parameter
#         param_value = health_metric_update.value
#         print(id, param_name, param_value)
#         data = utils.append_parameter_schema(param_name,param_value)
#         pots_collection.document(id).update(data)
#         return {"success": True}
#     except Exception as e:
#         return f"An Error Occured: {e}"


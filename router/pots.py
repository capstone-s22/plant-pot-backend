import sys
from fastapi import APIRouter
from models.Pot import NewPot, HealthMetricUpdate
from lib import utils

from lib.firebase import pots_collection

sys.path.append("..")
from ws import ws_pots
from requests import get
router = APIRouter()

@router.get('/health')
async def create():
    try:
        ip = get('https://api.ipify.org').text
        print('My public IP address is: {}'.format(ip))
        ws_pots.manager.check_existing_connections()
        await ws_pots.manager.broadcast("Broadcast")
        return {"health check": True}
    except Exception as e:
        return f"An Error Occured: {e}"

@router.post('/add')
async def create(new_pot: NewPot):
    try:
        id = new_pot.id
        data = utils.create_new_pot_schema(id)
        pots_collection.document(id).set(data)
        return {"success": True}
    except Exception as e:
        return f"An Error Occured: {e}"

@router.put('/update')
async def update(health_metric_update: HealthMetricUpdate):
    try:
        id = health_metric_update.id
        param_name = health_metric_update.parameter
        param_value = health_metric_update.value
        data = utils.update_parameter_schema(param_name,param_value)
        pots_collection.document(id).update(data)
        return {"success": True}
    except Exception as e:
        return f"An Error Occured: {e}"

@router.post('/append')
async def append(health_metric_update: HealthMetricUpdate):
    try:
        id = health_metric_update.id
        param_name = health_metric_update.parameter
        param_value = health_metric_update.value
        print(id, param_name, param_value)
        data = utils.append_parameter_schema(param_name,param_value)
        pots_collection.document(id).update(data)
        return {"success": True}
    except Exception as e:
        return f"An Error Occured: {e}"


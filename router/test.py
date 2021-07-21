import sys
from fastapi import APIRouter
from lib.custom_logger import logger

router = APIRouter()

@router.get('/test')
async def test():
    try:
        return {"success": True}

    except Exception as e:
        logger.error(e)
        return {"success": False}
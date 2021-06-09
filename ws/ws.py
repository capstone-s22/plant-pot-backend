from fastapi import WebSocket, APIRouter
import asyncio

from lib.firebase import pots_collection

TO_NOTIFY_POT = False

router = APIRouter()

@router.websocket('/health')
async def health_check(websocket: WebSocket):
    global TO_NOTIFY_POT
    try:
        await websocket.accept()
        count = 0
        while True:
            print(TO_NOTIFY_POT)
            # data = await websocket.receive_json()
            # print(data)
            await asyncio.sleep(3)
            if TO_NOTIFY_POT:
                await websocket.send_text("Changed {}".format(count))
            else:
                await websocket.send_text("No change {}".format(count))
            count += 1
    except Exception as e:
        return f"An Error Occured: {e}"


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if TO_NOTIFY_POT:
            await websocket.send_text(f"Data received!")
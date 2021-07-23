from dotenv import load_dotenv
load_dotenv()

import sys
from fastapi import FastAPI
import uvicorn

from lib.custom_logger import logger
from ws import ws_server
from router import pots, plants, test, check_in, quiz, sensor
from scheduler import scheduler
# Initialize FastAPI app

app = FastAPI()
app.include_router(test.router)
app.include_router(pots.router)
app.include_router(sensor.router)
app.include_router(plants.router)
app.include_router(check_in.router)
app.include_router(quiz.router)
app.include_router(ws_server.router)

logger.info("Server started")

if __name__ == '__main__':
    sys.exit("Run: `uvicorn main:app --reload --port 8000` instead")
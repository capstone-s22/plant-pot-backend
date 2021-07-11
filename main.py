from dotenv import load_dotenv
load_dotenv()

import sys
from fastapi import FastAPI
import uvicorn

from ws import ws_server, firebase_listener
from router import pots, plants
from scheduler import scheduler
from lib import check_in
# Initialize FastAPI app


app = FastAPI()

app.include_router(pots.router)
app.include_router(plants.router)
app.include_router(ws_server.router)

if __name__ == '__main__':
    sys.exit("Run: `uvicorn main:app --reload --port 8000` instead")
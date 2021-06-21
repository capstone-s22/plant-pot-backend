import sys
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

from ws import ws_server
from router import pots
from scheduler import scheduler

# Initialize FastAPI app

load_dotenv()

app = FastAPI()

app.include_router(pots.router)
app.include_router(ws_server.router)

if __name__ == '__main__':
    sys.exit("Run: `uvicorn main:app --reload --port 8000` instead")
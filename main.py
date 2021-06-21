from fastapi import FastAPI
import uvicorn

from ws import ws_server
from router import pots
from scheduler import scheduler

# Initialize FastAPI app
app = FastAPI()

app.include_router(pots.router)
app.include_router(ws_server.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True, debug=True, log_level="debug")
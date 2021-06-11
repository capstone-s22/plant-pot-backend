from fastapi import FastAPI
import uvicorn

from router import pots
from ws import ws_pots
# Initialize FastAPI app
app = FastAPI()

app.include_router(pots.router)
app.include_router(ws_pots.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True, debug=True, log_level="debug")
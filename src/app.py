from fastapi import FastAPI

from .database import sqlite
from .routers import account, event

app = FastAPI()

app.include_router(account.router, prefix='/accounts')
app.include_router(event.router, prefix='/events')

@app.get('/health')
async def health():
    return "In good health!"

sqlite.setup()
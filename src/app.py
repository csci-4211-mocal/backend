from fastapi import FastAPI

from .database import sqlite
from .routers import account, contact, event

app = FastAPI()

app.include_router(account.router, prefix='/accounts')
app.include_router(contact.router, prefix='/contacts')
app.include_router(event.router, prefix='/events')

sqlite.setup()
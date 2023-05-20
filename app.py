from fastapi import FastAPI

from src.routers.router_trello import api_trello
from src.routers.router_telegram import api_telegram

app = FastAPI()

app.include_router(api_trello)
app.include_router(api_telegram)
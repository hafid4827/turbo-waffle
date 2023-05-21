from fastapi import FastAPI

from src.routers.router_telegram import api_telegram

app = FastAPI()

app.include_router(api_telegram)
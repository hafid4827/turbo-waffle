from fastapi import APIRouter

api_telegram = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)

@api_telegram.get("/telegram_send")
def telegram_home():
    return {"hola": "mundo trello"}

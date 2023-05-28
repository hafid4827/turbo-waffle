from fastapi import APIRouter, BackgroundTasks, Request

from src.keys.key_trello import PUBLIC_KEY, TOKEN_TRELLO, TOKEN_TELEGRAM
from src.controllers.controlle_trello import TelegramBot

trello = TelegramBot(
    public_key = PUBLIC_KEY,
    token_trello = TOKEN_TRELLO,
    token_telegram=TOKEN_TELEGRAM
)

api_telegram = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)

@api_telegram.post("/trello_users")
async def trello_user(requests: Request, background_tasks: BackgroundTasks):
    data = await requests.json()
    background_tasks.add_task(trello.handler_send_message, message=data)
    return {"message": "ok"}
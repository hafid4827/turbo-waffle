from src.keys.key_trello import PUBLIC_KEY, TOKEN, TOKEN_TELEGRAM

from fastapi import APIRouter

from src.controllers.controlle_trello import TelegramBot

trello = TelegramBot(
    public_key = PUBLIC_KEY,
    token_trello = TOKEN,
    token=TOKEN_TELEGRAM
)

api_telegram = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)

@api_telegram.get("/trello_users")
def trello_user():
    result_response = trello.filter_member_name_by_id()
    print(result_response)
    return "lo que sea"


@api_telegram.get("/telegram_send")
def telegram_home():
    return {"hola": "mundo trello"}

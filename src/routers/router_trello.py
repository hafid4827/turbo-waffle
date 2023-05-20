from fastapi import APIRouter

api_trello = APIRouter(
    prefix="/trello",
    tags=["Trello"],
)

@api_trello.get("/holamundo")
def holamundo():
    return {"hola": "mundo trello"}

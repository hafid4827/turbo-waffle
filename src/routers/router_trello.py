
from src.controllers.controlle_resume import template_resume

from fastapi import APIRouter, BackgroundTasks
from typing import Optional

api_trello = APIRouter(
    prefix="/trello",
    tags=["Trello"],
)

@api_trello.post("/resume")
def holamundo(
    text: str,
    backgound_task: BackgroundTasks
    ):
    backgound_task.add_task(template_resume, text)
    return {"status" : 200}

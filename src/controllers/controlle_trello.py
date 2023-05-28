import requests
from difflib import get_close_matches

from telebot import TeleBot

from gensim.summarization import summarize


class Trello:
    def __init__(self, public_key: str, token_trello: str) -> None:
        """
        :param public_key: str
        :param token_trello: str
        """
        self.public_key = public_key
        self.token_trello = token_trello
        self.url = "https://api.trello.com"
        self.params = {
            "key": self.public_key,
            "token": self.token_trello
        }

    def get_members_me_boards(self):
        """
        get all boards by members
        :return: list
        """
        endpoint = f"{self.url}/1/members/me/boards"
        response = requests.request(
            method="GET", url=endpoint, params=self.params)
        if not response.status_code == 200:
            return "no se logro la petiricon deseada"

        return response

    def get_board_info(self, id: str) -> list:
        """
        get all boards by members
        params: id -> id board
        :return: list of boards
        """
        endpoint = f"{self.url}/1/boards/{id}/lists"
        response = requests.request(
            method="GET", url=endpoint, params=self.params)
        if not response.status_code == 200:
            return "no se logro la petiricon deseada"
        return response.json()

    def get_list_info(self, id_list: str) -> list:
        endpoint = f"{self.url}/1/lists/{id_list}/cards"
        response = requests.request(
            method="GET", url=endpoint, params=self.params)
        if not response.status_code == 200:
            return "no se logro la petiricon deseada"
        return response.json()

    def get_members(self, _id: str):
        endpoint = f"{self.url}/1/members/{_id}"
        response = requests.request(
            method="GET", url=endpoint, params=self.params)
        if not response.status_code == 200:
            return "no se logro la petiricon deseada"
        return response.json()


class FiltersTrelloEnpoints(Trello):
    def __init__(self, public_key: str, token_trello: str) -> None:
        super().__init__(public_key, token_trello)

    def filter_members_me_boards(self) -> str or bool:
        response = self.get_members_me_boards()

        if type(response) == str:
            return False

        response_list = response.json()
        response_filter = [
            itemm_repose.get("id") for itemm_repose in response_list
            if itemm_repose.get("name") == "autimatizacion_1"
        ]
        return response_filter[0]

    def filter_colums_by_board(self):
        _id = self.filter_members_me_boards()
        respose = self.get_board_info(id=_id)
        response_filter = [item_repose.get("id") for item_repose in respose]
        return response_filter

    def filter_resume(self, response):
        if not bool(response):
            return None

        for item_task in response:
            list_flield = {
                "name": item_task.get("name"),
                "link": item_task.get("shortUrl"),
                "description": item_task.get("desc"),
                "dateLastActivity": item_task.get("dateLastActivity"),
                "idMembers": item_task.get("idMembers"),
            }
        return list_flield

    def filter_card_by_colums(self):
        _ids = self.filter_colums_by_board()
        task_list_filter = []
        for _id in _ids:
            respose = self.get_list_info(id_list=_id)
            list_flield = self.filter_resume(response=respose)
            task_list_filter.append(list_flield)
        return task_list_filter

    def filter_member_name_by_id(self):
        members = self.filter_card_by_colums()
        counter = 0
        for item_member in members:
            list_members_by_task = item_member.get("idMembers")
            list_temporal = []
            for id_member in list_members_by_task:
                get_full_name = self.get_members(id_member)
                if not type(get_full_name) == str:
                    full_name = get_full_name.get("fullName")
                    list_temporal.append(full_name)
            members[counter]["idMembers"] = list_temporal
            counter += 1
        return members
    
    def template_resume(self, text: str) -> dict:
        summary = summarize(text)
        result_filter = {
            "lenght_letter": len(summary),
            "lenght_words": len(summary.split()),
            "text": summary
        }
        return result_filter
    
    def has_multiple_sences(self, text:str):
        sentence  = ".!?"
        sentence_count = sum(text.count(item_senetence) for item_senetence in sentence)
        return sentence_count > 1


    def resume_contact(self):
        members_info = self.filter_member_name_by_id()
        data_info = ""
        for member in members_info:
            name = member.get("name")
            link = member.get("link")
            message_text = member.get("description")
            fine_multiple_sences = self.has_multiple_sences(text=message_text)
            if not fine_multiple_sences:
                continue
            description = self.template_resume(message_text)
            description_text = description.get("text")
            dateLastActivity =  "".join(member.get("dateLastActivity"))
            idMembers = ",".join(member.get("idMembers")) 
            data_info += f"name:{name}\nlink:{link}\ndescription:{description_text}\ndateLastActivity:{dateLastActivity} \n idMembers: {idMembers}\n\n"
        return data_info


class TelegramBot(FiltersTrelloEnpoints):
    def __init__(self, public_key: str, token_trello: str, token_telegram:str) -> None:
        super().__init__(public_key, token_trello)
        self.token_telegram = token_telegram
        self.bot = TeleBot(self.token_telegram)
        self.bot.set_webhook(url="https://008c-8-242-155-18.ngrok-free.app/telegram/trello_users")
    
    def find_similar(self, word: str, list_words: list) -> str:
        result = get_close_matches(word, list_words)
        return result

    def handler_send_message(self, message: str) -> None:
        message_id_chat = message["message"]["chat"]["id"]
        message_text = message["message"]["text"]
        message_text_split = message_text.split(" ")
        find_similar = self.find_similar(
            word="dame un resumen",
            list_words=message_text_split
        )
        text_trello = self.resume_contact()
        if find_similar and text_trello:
            self.bot.send_message(chat_id=message_id_chat, text=text_trello)
        return None
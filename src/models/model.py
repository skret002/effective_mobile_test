import json
import os
import sys
from abc import ABC
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

load_dotenv()

from utils.work_whith_file import (  # noqa: E402
    delete_json_post,
    get_new_id,
    read_json_file,
    write_json_file,
)



class TypeOperationEnum(str, Enum):
    operation_income = os.getenv("CATEGORY_INCOME_NAME")
    operation_consumption = os.getenv("CATEGORY_CONS_NAME")


@dataclass
class Post(ABC):
    """ Базовый класс для записей. По сути DTO"""
    id: int = field(default=0)
    category: TypeOperationEnum = field(default=TypeOperationEnum.operation_consumption)
    current_date: datetime = field(
        default_factory=lambda: datetime.now().date().isoformat()
    )
    value:float = field(default=0.0)
    description:str = field(default=None)
    note:str = field(default=None)


class WalletAction():
    """Класс для операций с кошельком"""
    def __init__(self) -> None:
        self.name_app = 'Wallet'

    @staticmethod
    def dict_to_template(data: dict) -> list:
        """Приводим данные к читаемому виду для юзера"""
        text_tamplate = []
        for post in data:
            text_tamplate.append(
                [f"Id: {post.id } Дата: {post.current_date}  Категория: {post.category}  Cумма: {post.value} \
                    Описание: {post.description} Примечание: {post.note}"
                ]
            )
        return text_tamplate

    @classmethod
    def check_balance(cls) -> dict:
        """Проверка баланса, на вход ничего не принимает, отдает общий баланс и отдельно расход/доход """
        all_post = cls.encode_json_to_post_dataclass(read_json_file())
        if all_post:
            income = sum(list(map(lambda x: x.value if x.category == TypeOperationEnum.operation_income else 0, all_post)))
            consumption = sum(list(map(lambda x: x.value if x.category == TypeOperationEnum.operation_consumption else 0, all_post)))
            balance = income - consumption
            return {"balance": balance, "income": income, "consumption": consumption}

    @classmethod
    def write_data(cls,new_data: dict) -> str:
        """Зпись поста"""
        if new_data["category"] and new_data["value"]:
            new_post = Post()
            new_post.id = new_data.get("id", get_new_id())
            new_post.category = new_data["category"]
            new_post.value = abs(new_data["value"])
            new_post.description = new_data["description"]
            new_post.note = new_data["note"]
            write_json_file(new_post)
            return('Данные внесены')
        return('Ошибка внесения данных')

    @classmethod
    def get_post(cls, search_id:int) -> dict:
        """Получение одного поста по id, на вход только число"""
        match_data = next(
            (item for item in read_json_file() if item["id"] == search_id), None
        )
        return match_data

    @classmethod
    def search_data(cls, looking_word: str) ->dataclass:
        """Поиск по записям, принимает любую строку, но даты через дефиз 2024-07"""
        all_posts = cls.encode_json_to_post_dataclass(read_json_file())
        found = []
        for post in all_posts:
            match_data = any(str(looking_word) in str(value) for value in asdict(post).values())
            if match_data:
                found.append(post)
        return WalletAction.dict_to_template(found)

    @classmethod
    def get_some_last_post(cls, slice = -5) -> list:
        """Получение нескольктх записей, дефолтно последнии 5"""
        last_posts = cls.encode_json_to_post_dataclass(read_json_file())[slice:]
        tamplate = WalletAction.dict_to_template(last_posts)
        return tamplate

    @classmethod
    def delete_post(cls, id:int) -> str:
        """Удаление поста по ID, если None то удалит все"""
        result = delete_json_post(id)
        return result

    @staticmethod
    def encode_json_to_post_dataclass(data: json) -> dataclass:
        """Json to DATACLASS"""
        json_data = read_json_file()
        all_post = []
        if json_data:
            for item in json_data:
                post = Post(
                    id=item["id"],
                    category=item["category"],
                    current_date=item["current_date"],
                    value=item["value"],
                    description=item["description"],
                    note=item["note"],
                )
                all_post.append(post)
        return all_post

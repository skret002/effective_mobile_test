
import os
import random
import sys

import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.models.model import WalletAction


@pytest.fixture
def wallet_data():
    categories = ["Доход", "Расход"]
    descriptions = ["Зарплата", "Аренда", "Продукты", "Развлечения", "Бензин","Жена","Кошка"]
    notes = [
        "Ежемесячная выплата",
        "Ежемесячный платеж",
        "Еженедельные покупки",
        "Развлечения на выходных",
        "Проезд на работу",
        "Так случилось :)"
    ]

    data = []
    for _ in range(10):
        category = random.choice(categories)
        value = round(random.uniform(100.0, 5000.0), 2)
        description = random.choice(descriptions)
        note = random.choice(notes)
        record = {
            "category": category,
            "value": value,
            "description": description,
            "note": note,
        }
        data.append(record)

    return data


def test_write_data(wallet_data):
    result = WalletAction.write_data(wallet_data[0])
    assert result == "Данные внесены"

def test_check_balance():
    result = WalletAction.check_balance()
    assert isinstance(result, dict)
    assert "balance" in result
    assert "income" in result
    assert "consumption" in result
    assert "income" in result
    assert "consumption" in result
    assert "consumption" in result


def test_get_post():
    post = WalletAction.get_post(1)
    assert isinstance(post, dict)
    assert "category" in post
    assert "value" in post
    assert "description" in post
    assert "note" in post

def test_delete_post():
    result = WalletAction.delete_post(1)
    assert result == "Данные успешно удалены"
    result = WalletAction.delete_post(None)
    assert result == "Данные успешно удалены"


def test_search_data(wallet_data):
    WalletAction.delete_post(None)
    random_data = wallet_data[random.randint(0, 5)]
    WalletAction.write_data(random_data)
    results = WalletAction.search_data(random_data["description"])
    results2 = WalletAction.search_data(str(random_data["value"]))
    assert isinstance(results, list)
    assert len(results) > 0
    assert random_data["description"] in results[0][0]
    assert str(random_data["value"]) in results2[0][0]


def test_get_some_last_post(wallet_data):
    for i in range(0,5):
        WalletAction.write_data(wallet_data[i])
    results = WalletAction.get_some_last_post()
    assert isinstance(results, list)
    assert len(results) == 5



def test_delete_all_posts():
    result = WalletAction.delete_post(None)
    assert result == "Все записи успешно удалены." or "Данные успешно удалены"
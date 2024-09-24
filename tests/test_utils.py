import pytest
from _datetime import datetime

from src.utils import get_greeting, get_top_5_transactions, process_card_data


def test_top_5_transactions(transactions):
    expected = [
        {"date": "2021-01-06", "amount": 600.0, "category": "Тест", "description": "Тестовая транзакция 6"},
        {"date": "2021-01-05", "amount": 500.0, "category": "Тест", "description": "Тестовая транзакция 5"},
        {"date": "2021-01-04", "amount": 400.0, "category": "Тест", "description": "Тестовая транзакция 4"},
        {"date": "2021-01-03", "amount": 300.0, "category": "Тест", "description": "Тестовая транзакция 3"},
        {"date": "2021-01-02", "amount": 200.0, "category": "Тест", "description": "Тестовая транзакция 2"},
    ]
    result = get_top_5_transactions(transactions)
    assert result == expected


def test_less_than_5_transactions(transactions):
    fewer_transactions = transactions[:3]
    expected = [
        {"date": "2021-01-03", "amount": 300.0, "category": "Тест", "description": "Тестовая транзакция 3"},
        {"date": "2021-01-02", "amount": 200.0, "category": "Тест", "description": "Тестовая транзакция 2"},
        {"date": "2021-01-01", "amount": 100.0, "category": "Тест", "description": "Тестовая транзакция 1"},
    ]
    result = get_top_5_transactions(fewer_transactions)
    assert result == expected


def test_empty_transactions():
    result = get_top_5_transactions([])
    assert result == []


@pytest.mark.parametrize(
    "expected_output",
    [
        [
            {"last_digit": "7197", "total_spent:": 300.0, "cashback": 3.0},
            {"last_digit": "5091", "total_spent:": 450.0, "cashback": 4.0},
            {"last_digit": "4556", "total_spent:": 50.0, "cashback": 0},
        ]
    ],
)
def test_process_card_data(transactions_for_process_card_data, expected_output):
    result = process_card_data(transactions_for_process_card_data)
    assert result == expected_output


@pytest.mark.parametrize(
    "current_time, expected_greeting",
    [
        (datetime(2023, 1, 1, 6, 0), "Доброе утро"),  # Утро
        (datetime(2023, 1, 1, 12, 0), "Добрый день"),  # Полдень
        (datetime(2023, 1, 1, 16, 59), "Добрый день"),  # Днём
        (datetime(2023, 1, 1, 17, 0), "Добрый вечер"),  # Вечером
        (datetime(2023, 1, 1, 21, 59), "Добрый вечер"),  # Вечером
        (datetime(2023, 1, 1, 22, 0), "Доброй ночи"),  # Ночью
        (datetime(2023, 1, 1, 4, 59), "Доброй ночи"),  # Поздно ночью
    ],
)
def test_get_greeting(current_time, expected_greeting):
    assert get_greeting(current_time) == expected_greeting


if __name__ == "__main__":
    pytest.main()

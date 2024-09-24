import json

import pytest

from src.services import find_phone_numbers


@pytest.mark.parametrize(
    "expected_phone, expected_count",
    [
        ("+7 921 111-22-33", 1),  # Проверка одного номера телефона
        ("+7 995 555-55-55", 1),  # Проверка другого номера телефона
        ("+7 981 333-44-55", 1),  # Проверка третьего номера телефона
        ("магазине", 0),  # Проверка транзакции без номера телефона
    ],
)
def test_find_phone_numbers(transactions_for_find_phone_numbers, expected_phone, expected_count):
    """Параметризированный тест для поиска номеров телефонов."""
    result = find_phone_numbers(transactions_for_find_phone_numbers)
    parsed_result = json.loads(result)

    # Вывод для отладки
    print(f"Найденные транзакции: {parsed_result}")

    # Проверяем, что ожидаемый номер телефона найден
    found_phones = [tran["Описание"] for tran in parsed_result if expected_phone in tran["Описание"]]
    assert len(found_phones) == expected_count

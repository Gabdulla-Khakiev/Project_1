import json
import logging
import re

# Регулярное выражение для поиска номеров телефонов
PHONE_REGEX = r"\+7\s\d{3}\s\d{3}-\d{2}-\d{2}"

# Настройка логирования
logging.basicConfig(filename="services.log", level=logging.INFO)


def find_phone_numbers(transactions: list) -> str:
    """Ищет номера телефонов в описаниях транзакций и возвращает результат в формате JSON."""

    def has_phone(transaction):
        description = transaction.get("Описание", "")
        match = re.search(PHONE_REGEX, description)
        if match:
            logging.info(f"Найден номер телефона: {match.group()}")
        return match is not None

    # Фильтрация транзакций с номерами телефонов
    phone_transactions = list(filter(has_phone, transactions))

    # Логируем количество найденных транзакций
    logging.info(f"Найдено {len(phone_transactions)} транзакций с номерами телефонов.")

    # Преобразование результата в JSON-формат
    return json.dumps(phone_transactions, ensure_ascii=False, indent=4)

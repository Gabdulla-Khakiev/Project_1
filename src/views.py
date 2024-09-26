import json
import logging

from _datetime import datetime

from src.external_api import get_exchange_rate, get_sp500_stock_price
from src.file_readers import read_transactions_from_excel
from src.utils import get_greeting, get_top_5_transactions, process_card_data

file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[file_handler])


def load_user_settings(file_path: str = "data/user_settings.json") -> dict:
    """Загружает пользовательские настройки из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return {}
    except json.JSONDecodeError:
        print("Ошибка в формате JSON.")
        return {}


settings = list(load_user_settings().get("user_currencies"))
snp_settings = list(load_user_settings().get("user_stocks"))


def get_date_range(date_str: str) -> tuple:
    """Возвращает диапазон дат от начала месяца до указанной даты."""
    input_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%Ss")
    start_of_month = input_date.replace(day=1)
    return start_of_month, input_date


def generate_report(datetime_str: str, transactions: list) -> str:
    """Формирует JSON-ответ на основе данных."""
    # Парсинг даты
    current_time = datetime.now()

    # Получаем приветствие
    greeting = get_greeting(current_time)

    # Получаем информацию по картам
    card_info = process_card_data(transactions)

    # Получаем топ-5 транзакций
    top_5_transactions = get_top_5_transactions(transactions)

    # Получаем курс валют ( -> RUB)
    exchange_rate = list(map(get_exchange_rate, settings))

    # Получаем стоимость акции из S&P 500
    sp500_price = list(map(get_sp500_stock_price, snp_settings))

    # Формируем финальный результат в формате JSON
    response = {
        "greeting": greeting,
        "cards": card_info,
        "top_transactions": top_5_transactions,
        "currency_rates": exchange_rate,
        "stock_prices": sp500_price,
    }

    return json.dumps(response, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    transactions = read_transactions_from_excel("data/operations.xlsx")
    date_str = "2020-05-20 14:30:00"
    result = generate_report(date_str, transactions)
    print(result)

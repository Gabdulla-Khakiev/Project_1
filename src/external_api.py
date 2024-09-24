import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Настраиваем формат логов
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

BASE_EXCHANGES_URL = "https://api.apilayer.com/exchangerates_data/latest"
EXCHANGES_API = os.getenv("EXCHANGES_API")

BASE_SNP_URL = "https://www.alphavantage.co/query"
SNP_API = os.getenv("SNP_API")


def get_exchange_rate(from_currency, to_currency="RUB"):
    """Получает курс валюты через Exchange Rates Data API."""
    url = f"{BASE_EXCHANGES_URL}?symbols={to_currency}&base={from_currency}"
    headers = {"apikey": EXCHANGES_API}

    try:
        logging.info(f"Запрос курса валют: {from_currency} -> {to_currency}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка статуса ответа
        data = response.json()

        if data.get("success") and "rates" in data:
            base = data.get("base")
            rates = data.get("rates").get(to_currency)
            logging.info(f"Успешно получен курс валют: {from_currency} -> {to_currency}: {rates}")
            return {"base": base, "rates": rates}
        else:
            logging.error(f"Ошибка в данных курса валют: {data}")
            return None

    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе курса валют: {e}")
        return None


def get_sp500_stock_price(symbol):
    """Возвращает текущую стоимость акции из S&P 500."""
    url = f"{BASE_SNP_URL}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={SNP_API}"

    try:
        logging.info(f"Запрос стоимости акции: {symbol}")
        response = requests.get(url)
        response.raise_for_status()  # Проверка статуса ответа
        data = response.json()
        price = data.get("Global Quote", {}).get("05. price")

        if price:
            logging.info(f"Стоимость акции {symbol}: {price}")
            return {"stock": symbol, "price": price}
        else:
            logging.error(f"Не удалось получить стоимость акции {symbol}. Данные: {data}")
            return 0.0
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе стоимости акции {symbol}: {e}")
        return 0.0

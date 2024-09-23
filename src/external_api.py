import requests
import os
from src.views import load_user_settings
from dotenv import load_dotenv

load_dotenv()

BASE_EXCHANGES_URL = 'https://api.apilayer.com/exchangerates_data/latest'
EXCHANGES_API = os.getenv("EXCHANGES_API")

BASE_SNP_URL = 'https://www.alphavantage.co/query'
SNP_API = os.getenv('SNP_API')


def get_exchange_rate(from_currency, to_currency="RUB"):
    """Получает курс валюты через Exchange Rates Data API."""
    url = f"{BASE_EXCHANGES_URL}?symbols={to_currency}&base={from_currency}"
    headers = {"apikey": EXCHANGES_API}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        base = data.get("base")
        rates = data.get("rates").get("RUB")

        if data.get("success") and "rates" in data:
            base = data.get("base")
            rates = data.get("rates").get(to_currency)

        if base and rates is not None:
            return {"base": base, "rates": rates}

    except requests.RequestException as e:
        print(f"Ошибка при получении курса валют: {e}")
        return None


def get_sp500_stock_price(symbol) -> float:
    """Возвращает текущую стоимость акции из S&P 500."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': SNP_API
    }
    url = f"{BASE_SNP_URL}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={SNP_API}"
    response = requests.get(url)
    data = response.json()
    # return float(data["Global Quote"]["05. price"])
    return data


if __name__ == "__main__":
    snp_settings = list(load_user_settings().get('user_stocks'))
    print(get_sp500_stock_price(snp_settings))

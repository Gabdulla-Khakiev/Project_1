import pandas as pd
import pytest


@pytest.fixture()
def transactions():
    return [
        {
            "Дата платежа": "2021-01-01",
            "Сумма операции с округлением": 100.0,
            "Сумма платежа": 100.0,
            "Категория": "Тест",
            "Описание": "Тестовая транзакция 1",
        },
        {
            "Дата платежа": "2021-01-02",
            "Сумма операции с округлением": 200.0,
            "Сумма платежа": 200.0,
            "Категория": "Тест",
            "Описание": "Тестовая транзакция 2",
        },
        {
            "Дата платежа": "2021-01-03",
            "Сумма операции с округлением": 300.0,
            "Сумма платежа": 300.0,
            "Категория": "Тест",
            "Описание": "Тестовая транзакция 3",
        },
        {
            "Дата платежа": "2021-01-04",
            "Сумма операции с округлением": 400.0,
            "Сумма платежа": 400.0,
            "Категория": "Тест",
            "Описание": "Тестовая транзакция 4",
        },
        {
            "Дата платежа": "2021-01-05",
            "Сумма операции с округлением": 500.0,
            "Сумма платежа": 500.0,
            "Категория": "Тест",
            "Описание": "Тестовая транзакция 5",
        },
        {
            "Дата платежа": "2021-01-06",
            "Сумма операции с округлением": 600.0,
            "Сумма платежа": 600.0,
            "Категория": "Тест",
            "Описание": "Тестовая транзакция 6",
        },
    ]


@pytest.fixture
def transactions_for_process_card_data():
    """Фикстура с тестовыми транзакциями."""
    return [
        {"Номер карты": "*7197", "Сумма операции с округлением": 100},
        {"Номер карты": "*7197", "Сумма операции с округлением": 200},
        {"Номер карты": "*5091", "Сумма операции с округлением": 150},
        {"Номер карты": "*5091", "Сумма операции с округлением": 300},
        {"Номер карты": "*4556", "Сумма операции с округлением": 50},
        {"Номер карты": None, "Сумма операции с округлением": 500},
    ]


@pytest.fixture
def transactions_for_find_phone_numbers():
    """Возвращает список транзакций для тестов."""
    return [
        {"Описание": "Я МТС +7 921 111-22-33", "Сумма операции": -300},
        {"Описание": "Тинькофф Мобайл +7 995 555-55-55", "Сумма операции": -500},
        {"Описание": "Покупка в магазине", "Сумма операции": -1000},
        {"Описание": "МТС Mobile +7 981 333-44-55", "Сумма операции": -1500},
    ]


@pytest.fixture
def transactions_for_reports():
    """Создает тестовый датафрейм с транзакциями."""
    data = {
        "Дата операции": ["2023-06-01", "2023-07-15", "2023-08-20", "2023-09-01"],
        "Категория": ["Продукты", "Продукты", "Развлечения", "Продукты"],
        "Сумма операции": [-1500.0, -2000.0, -500.0, -1000.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_transactions():
    return pd.DataFrame(
        {
            "Номер карты": ["*1234", "*5678"],
            "Сумма операции с округлением": [100.50, 200.75],
            "Категория": ["Покупки", "Снятие наличных"],
            "Описание": ["Покупка продуктов", "Снятие в банкомате"],
        }
    )


@pytest.fixture
def transactions_for_views():
    return [
        {"Номер карты": "*5814", "Сумма операции с округлением": 1262.00},
        {"Номер карты": "*7512", "Сумма операции с округлением": 7.94},
        {
            "date": "21.12.2021",
            "amount": 1198.23,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
        {"date": "20.12.2021", "amount": 421.00, "category": "Различные товары", "description": "Ozon.ru"},
        {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
        {"date": "16.12.2021", "amount": 453.00, "category": "Бонусы", "description": "Кешбэк за обычные покупки"},
    ]

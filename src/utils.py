import logging
from datetime import datetime
from src.file_readers import read_transactions_from_excel


file_handler = logging.FileHandler('app.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[file_handler])


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 5 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 17:
        greeting = "Добрый день"
    elif 17 <= hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    logging.info(f"Время: {current_time}, Приветствие: {greeting}")
    return greeting
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def process_card_data(transactions):
    """Возвращает данные по каждой карте: последние 4 цифры, общая сумма и кешбэк."""
    cards_information = []
    cards_summary = {}

    logging.info(f"Обработка {len(transactions)} транзакций.")

    for transaction in transactions:
        card_number = transaction.get("Номер карты", "")

        if isinstance(card_number, str) and len(str(card_number)) >= 4:
            try:
                amount = float(transaction.get("Сумма операции с округлением", 0))
                # Если карта уже есть в словаре, добавляем сумму, иначе создаем запись
                if card_number in cards_summary:
                    cards_summary[card_number] += amount
                else:
                    cards_summary[card_number] = amount
            except ValueError as e:
                logging.error(f"Ошибка при обработке суммы транзакции для карты {card_number}: {e}")
                continue
            # Получаем сумму операции
            amount = float(transaction.get("Сумма операции с округлением"))
            # Если карта уже есть в словаре, добавляем сумму, иначе создаем запись
            if card_number in cards_summary:
                cards_summary[card_number] += amount
            else:
                cards_summary[card_number] = amount

    cards_summ = [{"Номер карты": key, "Сумма трат": value} for key, value in cards_summary.items()]

    for t in cards_summ:
        total_spent = t.get("Сумма трат", 0)

        if total_spent > 0:  # Проверяем, чтобы сумма была больше нуля
            card_info = {
                "last_digit": t.get("Номер карты")[-4:],
                "total_spent:": total_spent,
                "cashback": total_spent // 100
            }

            logging.info(
                f"Данные по карте {t.get('Номер карты')[-4:]}: Траты - {total_spent}, Кэшбэк - {card_info['cashback']}")
            cards_information.append(card_info)

    logging.info(f"Обработаны данные по {len(cards_information)} картам.")
            cards_information.append(card_info)

    return cards_information


def get_top_5_transactions(transactions: list) -> list:
    """Возвращает топ-5 транзакций по сумме платежа."""
    try:
        logging.info("Сортировка транзакций по сумме.")
        sorted_transactions = sorted(transactions, key=lambda x: float(x.get('Сумма операции с округлением', 0)),
                                     reverse=True)
        top_5 = sorted_transactions[:5]
        logging.info(f"Топ-5 транзакций: {top_5}")

        formatted_transactions = []
        for t in top_5:
            transaction = {
                "date": t.get("Дата платежа"),
                "amount": t.get("Сумма операции с округлением"),
                "category": t.get("Категория"),
                "description": t.get("Описание")
            }
            formatted_transactions.append(transaction)
        return formatted_transactions
    except Exception as e:
        logging.error(f"Ошибка при сортировке транзакций: {e}")
        return []
    sorted_transactions = []
    transactions = sorted(transactions, key=lambda x: float(x.get('Сумма операции с округлением')), reverse=True)
    for t in transactions:
        transaction = {
            "date": t.get("Дата платежа"),
            "amount": t.get("Сумма платежа"),
            "category": t.get("Категория"),
            "description": t.get("Описание")
        }
        sorted_transactions.append(transaction)
    return sorted_transactions[:5]


if __name__ == "__main__":
    transactions = read_transactions_from_excel('data/operations.xlsx')
    print(process_card_data(transactions))

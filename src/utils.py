from datetime import datetime
from src.file_readers import read_transactions_from_excel


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 5 <= hour < 12:
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

    for transaction in transactions:
        card_number = transaction.get("Номер карты", "")

        if isinstance(card_number, str) and len(str(card_number)) >= 4:
            # Получаем сумму операции
            amount = float(transaction.get("Сумма операции с округлением"))
            # Если карта уже есть в словаре, добавляем сумму, иначе создаем запись
            if card_number in cards_summary:
                cards_summary[card_number] += amount
            else:
                cards_summary[card_number] = amount

    cards_summ = [{"Номер карты": key, "Сумма трат": value} for key, value in cards_summary.items()]

    for t in cards_summ:
        total_spent = t.get("Сумма трат")
        if total_spent > 0:  # Проверяем, чтобы сумма была больше нуля
            card_info = {
                "last_digit": t.get("Номер карты")[-4:],
                "total_spent:": total_spent,
                "cashback": total_spent // 100
            }

            cards_information.append(card_info)

    return cards_information


def get_top_5_transactions(transactions: list) -> list:
    """Возвращает топ-5 транзакций по сумме платежа."""
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

import pandas as pd


def read_transactions_from_excel(file_path: str):
    """Читает данные из Excel и возвращает их в виде списка словарей."""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        transactions = df.to_dict(orient='records')  # Преобразуем в список словарей
        return transactions
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка чтения Excel-файла: {e}")
        return []


if __name__ == "__main__":
    transactions = read_transactions_from_excel("data/operations.xlsx")
    print(transactions)


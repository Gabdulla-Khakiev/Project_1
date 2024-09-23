import pytest
from src.file_readers import read_transactions_from_excel
from unittest import mock


# Параметризация для различных путей файла
@pytest.mark.parametrize("file_path, expected_count", [
    ("data/operations.xlsx", 2),  # Успешное чтение файла
])
def test_read_transactions_from_excel(file_path, expected_count, mock_transactions):
    # Мокаем функцию pd.read_excel для возврата фиктивного DataFrame
    with mock.patch('pandas.read_excel', return_value=mock_transactions):
        transactions = read_transactions_from_excel(file_path)
        assert len(transactions) == expected_count

# Тест для проверки ошибки, когда файл не найден
def test_read_transactions_from_excel_file_not_found():
    transactions = read_transactions_from_excel("data/non_existing_file.xlsx")
    assert transactions == []  # Ожидаем, что транзакций не будет при отсутствии файла

# Тест для проверки ошибки при чтении
def test_read_transactions_from_excel_error(mock_transactions):
    # Мокаем ошибку при чтении файла
    with mock.patch('pandas.read_excel', side_effect=Exception("Ошибка чтения")):
        transactions = read_transactions_from_excel("data/operations.xlsx")
        assert transactions == []

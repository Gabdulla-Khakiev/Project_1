import pytest

from src.reports import spending_by_category


@pytest.mark.parametrize(
    "category, date, expected_total",
    [
        ("Продукты", "2023-09-15", -3000.0),  # Траты по категории "Продукты"
        ("Развлечения", "2023-09-15", -500.0),  # Траты по категории "Развлечения"
        ("Продукты", "2023-08-01", -3500.0),  # Траты по категории "Продукты" с более ранней датой
        ("Не существует", "2023-09-15", 0.0),  # Категория, которая отсутствует в транзакциях
    ],
)
def test_spending_by_category(transactions_for_reports, category, date, expected_total):
    """Параметризированный тест для функции траты по категории."""
    result = spending_by_category(transactions_for_reports, category, date)

    # Проверяем, что сумма трат соответствует ожидаемой
    assert result["total_expenses"] == expected_total

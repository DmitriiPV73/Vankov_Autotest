import pytest # Импортируем модуль pytest
from operations import multiply, divide # из файла operations.py импортируем для проверки функции multiply, divide

# === Фикстура === предоставляет 10 и 5 для использования в нескольких тестах
@pytest.fixture
def sample_numbers():
    """Фикстура, возвращающая пару чисел для тестов."""
    return 10, 5

# === Тесты умножения === в одной функции список кортежей для проверки
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-1, 5, -5),
    (0, 100, 0),
    (2.5, 4, 10.0),
    (-3, -7, 21)
])
def test_multiply(a, b, expected):
    """Проверка корректности умножения с разными входными данными."""
    assert multiply(a, b) == expected

# === Тесты деления === в одной функции список кортежей для проверки
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (-15, 0, -5.0),
    (7.5, 2.5, 3.0),
    (0, 1, 0.0)
])
def test_divide(a, b, expected):
    """Проверка корректности деления при допустимых значениях."""
    assert  divide(a, b) == expected

# === Тест исключения при делении на ноль ===
def test_divide_by_zero():
    """Проверка, что деление на ноль вызывает ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Деление на ноль запрещено."):
        divide(10, 0)


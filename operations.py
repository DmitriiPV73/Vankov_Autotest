def multiply(a: float, b: float) -> float:
    """Возвращает произведение двух чисел."""
    return a * b

def divide(a: float, b: float) -> float:
    """Возвращает результат деления a на b.
    Выбрасывает ZeroDivisionError, если b == 0.
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль запрещено.")
    return a / b
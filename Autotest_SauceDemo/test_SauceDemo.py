from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_successful_login():
    driver = webdriver.Chrome() # создаем экземпляр браузера Chrome
    wait = WebDriverWait(driver, 10) # создаем объект явного ожидания в 10 сек

    try:
        # Открыть главную страницу
        driver.get("https://www.saucedemo.com/")
        # assert "Swag Labs" in driver.title, "Заголовок страницы не совпадает"

        # Ввести логин
        user_login = driver.find_element(By.ID, "user-name") # находим элемент по ID "user-name"
        user_login.send_keys("standard_user") # вводим имя (логин) пользователя
        # assert user_login.get_attribute("value") == "standard_user" # Дополнительная валидация, проверка на значение имя

        # Ввести пароль
        user_pass = driver.find_element(By.ID, "password") # находим элемент по ID "password"
        user_pass.send_keys("secret_sauce") # вводим пароль пользователя
        # assert user_pass.get_attribute("value") == "secret_sauce" # Дополнительная валидация, проверка на значение пароля

        # Нажать кнопку Login
        button_login = driver.find_element(By.ID, "login-button") # находим элемент по ID "login-button"
        button_login.click() # нажимаем на кнопку
        wait.until(EC.url_contains("inventory.html")) # ждем 10 сек. для успешного перехода на страницу inventory.html

        # Проверить наличие заголовка Products
        title = driver.find_element(By.CLASS_NAME, "title") # находим элемент по имени "title" (заголовок)
        assert title.text == "Products", "Заголовок Products не найден" # проверяем, что текст заголовка "Products" найден

        print("Тест на авторизацию пройден успешно!") # если тест не упал раньше, выведет сообщение об успешном завершении
    finally:
        driver.quit() # закрываем браузер и освобождаем ресурсы

def test_product_to_cart(): # объявляем функцию теста, которая направляет товар в корзину
    driver = webdriver.Chrome() # создаем экземпляр браузера Chrome
    wait = WebDriverWait(driver, 10) # создаем объект явного ожидания в 10 сек

    try:
        # Авторизация (Pre-condition)
        driver.get("https://www.saucedemo.com/") # открываем главную страницу
        driver.find_element(By.ID, "user-name").send_keys("standard_user") # находим элемент с ID "user-name" и вводим "standard_user"
        driver.find_element(By.ID, "password").send_keys("secret_sauce") # находим элемент с ID "password" и вводим "secret_sauce"
        driver.find_element(By.ID, "login-button").click() # находим элемент с ID "login-button" и кликаем
        wait.until(EC.url_contains("inventory.html")) # ждем 10 сек. для успешного перехода на страницу inventory.html

        # Проверка, что список товаров загружен
        product_item = driver.find_elements(By.CLASS_NAME, "inventory_list") # находим элемент с имненем "inventory_list"
        assert len(product_item) > 0, "Список товаров пуст" # если список товаров не загрузиться, выпадет сообщение об ошибке



        # Выбор второго товара по xpach. Хрупкий вариант.
        product_cart = driver.find_element(By.XPATH, "(//button[contains(@class, 'btn_inventory')])[2]")
        product_name = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-test="inventory-item-name"]'))
        )
        item_name = product_name[1].text # Запоминаем имя продукта. [1]- "-1" - т.к. отсчет с "0"
        # print("\n Имя товара:", item_name)
        product_cart.click()

        # Проверка, что кнопка второго товара "Add to cart" поменяла текст на "Remove"
        # Необходимо вновь обратиться к полю кнопки второго товара, т.к. его состояние изменилось
        # В противном случае будет ошибка.
        product_cart = driver.find_element(By.XPATH, "(//button[contains(@class, 'btn_inventory')])[2]")
        assert product_cart.text == "Remove", "Кнопка не сменила статус на Remove"

        # Проверка бейджа корзины
        cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        assert cart_badge.text == "1", "Количество в корзине не равно 1"

        # Проверка наличия товара в корзине
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click() # находим элемент "shopping_cart_link" (корзина), кликаем
        cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        text_cart=cart_item.text # Запоминаем имя товара в корзине
        # print("\n Имя товара в корзине", text_cart)
        assert item_name == text_cart, "Товар не найден в корзине" # Проверка наименования товара

        print("Тест на выбор товара пройден успешно!")
    finally:
        driver.quit()

def test_complete_checkout(): # определяем функцию теста для оформления заказа
    driver = webdriver.Chrome() # создаем экземпляр браузера Chrome
    wait = WebDriverWait(driver, 10) # создаем объект явного ожидания в 10 сек

    try:
        # Авторизация и добавление товара в корзину
        driver.get("https://www.saucedemo.com/") # открываем главную страницу
        driver.find_element(By.ID, "user-name").send_keys("standard_user") # находим элемент с ID "user-name" и вводим "standard_user"
        driver.find_element(By.ID, "password").send_keys("secret_sauce") # находим элемент с ID "password" и вводим "secret_sauce"
        driver.find_element(By.ID, "login-button").click() # находим элемент с ID "login-button" и кликаем
        wait.until(EC.url_contains("inventory.html"))  # ждем 10 сек. для успешного перехода на страницу inventory.html
        product_cart = driver.find_element(By.XPATH, "(//button[contains(@class, 'btn_inventory')])[2]") # выбираем продукт
        product_cart.click() # заносим продукт в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()  # находим элемент "shopping_cart_link" (корзина), кликаем

        # Переход на страницу оформления заказа
        driver.find_element(By.ID, "checkout").click() # находим элемент с ID "checkout" (оформить заказ), кликаем
        assert "checkout" in driver.current_url, "Не произошел переход на страницу checkout"

        # Заполнить форму данных
        driver.find_element(By.ID, "first-name").send_keys("Petr") # находим элемент с ID "first-name", заполняем
        driver.find_element(By.ID, "last-name").send_keys("Ivanov") # находим элемент с ID "last-name", заполняем
        driver.find_element(By.ID, "postal-code").send_keys("123456") # находим элемент с ID "postal-code", заполняем

        # Нажать Continue
        driver.find_element(By.ID, "continue").click() # находим элемент с ID "continue", кликаем
        wait.until(EC.url_contains("checkout-step-two.html")) # ожидание 10 сек. пока не появиться "checkout-step-two"

        # Проверить заголовок Overview
        header = driver.find_element(By.CLASS_NAME, "title") # находим элемент по имени "title" (заголовок)
        assert header.text == "Checkout: Overview", "Заголовок страницы не совпадает" # проверяем, что текст заголовка "Checkout: Overview" найден

        print("Тест оформления заказа пройден успешно!")
    finally:
        driver.quit()
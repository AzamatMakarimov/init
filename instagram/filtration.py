from selenium import webdriver
import time
from datetime import datetime
import re

# исключения
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def two(days, acc_subscriptions, publications):
    browser = webdriver.Chrome("chromedriver.exe")
    today = datetime.now()

    # функция проверки существования элемента на странице(закрытый аккаунт)
    def xpath_existence(url):
        try:
            browser.find_element_by_xpath(url)
            existence = 1
        except NoSuchElementException:
            existence = 0
        return existence

    # считывание всех ссылок на пользователей из файла
    f =open("persons_list.txt", "r")
    file_list = []
    for line in f:
        file_list.append(line)
    f.close()

    # обработка ссылок
    filtered_list = [] # Фильтрованный список
    i = 0 # количество подходящих пользователей
    j = 0 # номер ввода в терминале

    for person in file_list:
        j += 1
        browser.get(person)
        time.sleep(2.7)

        # проверка на закрытость аккаунта
        element = "//section/main/div/div/article/div/div/h2"
        if xpath_existence(element) == 1:
            try:
                if browser.find_element_by_xpath(element).text == "This Account is Private" or "Это закрытый аккаунт":
                    continue
            except StaleElementReferenceException:
                xxx = 0

        # проверка на допустимое число подписок
        element = "//section/main/div/header/section/ul/li[3]/a/span"
        if xpath_existence(element) == 0:
            continue
        status = browser.find_element_by_xpath(element).text
        status = re.sub(r'\s', '', status) # удаление пробелов из числа подписок
        if int(status) > acc_subscriptions:
            continue

        # не должно быть ссылки на сайт //section/main/div/header/section/div[2]
        element = "//section/main/div/header/section/div[2]/span/a"
        if xpath_existence(element) == 1:
            continue

        # проверка на минимум публикаций
        element = "//section/main/div/header/section/ul/li[1]/a/span"
        if xpath_existence(element) == 0:
            continue
        status = browser.find_element_by_xpath(element).text
        status = re.sub(r'\s', '', status)  # удаление пробелов из числа публикаций
        if int(status) < publications:
            continue

        #  проверка на наличие аватарки
        element = "//section/main/div/header/div/div/span/img"
        if xpath_existence(element) == 0:
            continue
        status = browser.find_element_by_xpath(element).get_attribute("src")
        if status.find("s150x150") == 1:
            continue

        # проверка на дату последней публикации
        element = "//a[contains(@href, '/p')]"
        if xpath_existence(element) == 0:
            continue
        status = browser.find_element_by_xpath(element).get_attribute('href')
        browser.get(status)
        post_date = browser.find_element_by_xpath("//time").get_attribute('datetime')
        year = int(post_date[0:4])
        month = int(post_date[5:7])
        day = int(post_date[8:10])
        post_date = datetime(year, month, day)
        period = today - post_date
        if period.days > days:
            continue

        # Добавление пользователя в отфильтрованный список
        filtered_list.append(person)
        i += 1
        if i > 10:
            break

    f = open("filtered_persons_list.txt", "w")
    for line in filtered_list:
        f.write(line)
    f.close()

    # очистка файла неотфильтрованного списка
    f = open("persons_list.txt", "w")
    f.close()
    # выход
    browser.quit()

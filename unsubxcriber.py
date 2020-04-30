from selenium import webdriver
import time

# параметры
unsub_time = 80 # время между отписками (сек)
max = 0 # количество отписок, если 0 то все подписки бота


# исключения
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


# функция проверки существования элемента на странице
def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence

browser = webdriver.Chrome("chromedriver.exe")

# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login")
time.sleep(5)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(
    "89961063784")  # логин акаунта
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(
    "DVDazamat100007")  # пароль аккаунта
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()
time.sleep(7)

# чтение файла с подписками и сохранение данных в массив
file_list = []
f = open("filtered_persons_list.txt", "r")
for line in f:
    file_list.append(line)
f.close()

# процесс отписки
i = 0 # количество людей от которых мы отписались
for line in file_list:

    """# очистка пользователя в моих подписок
    f = open("my_subscriptions.txt", "r")
    r = 1
    text = set()
    while True:
        try:
            text.add(f.readline(r))
        except Exception:
            f.close()
            break
    text.remove(line)
    with open("my_subscriptions.txt", "w") as f:
        for w in text:
            f.writelines(w)"""

    i += 1
    if max != 0 and i == max + 1:
        break
    browser.get(line)
    element = "//section/main/div/header/section/div[1]/div[2]/span/span[1]/button"
    if xpath_existence(element) == 0:
        print("Ошибка 1 поиска кнопки отписки, либо вы не подписаны на аккаунт")
        continue

    try:
        button = browser.find_element_by_xpath(element)
    except StaleElementReferenceException:
        print("Ошибк 2 поиска кнопки отписки")
        continue

    if button.text != "Подписаться":
        try:
            button.click()
        except StaleElementReferenceException:
            print("Ошибка 3 нажатия кнопки отписки")
            continue

    if button.text == "Подписаться":
        print("вы уже подписаны на", line)
        continue
    time.sleep(1.3)

    element = "//div[4]/div/div/div[3]/button[1]"
    if xpath_existence(element) == 0:
        print("Ошибка 4 поиска кнопки отписки")
        continue

    button = browser.find_element_by_xpath(element)
    try:
        button.click()
    except StaleElementReferenceException:
        print("Ошибка:5 нажатия кнопки")
        continue
        
    print("Произвелась отписка от", line)
    time.sleep(unsub_time)

# завершение работы
browser.quit()

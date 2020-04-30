from selenium import webdriver
import time
import random
import re

# исключения
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

# параметры
like_time = 10  # время между лайками
all_likes = 900  # за сутки
all_subscriptions = 500  # за сутки
hour_like = 50  # максимальное число лайков за час
hour_sub = 50  # максимальное число подписок за час
z_likes = 2  # количество лайков которые мы ставим пользователю


random.seed

# В ЭТОМ ЧАСУ УЖЕ ЕСТЬ
likes = 0
subscribtions = 0

browser = webdriver.Chrome("chromedriver.exe")

# функция проверки существования элемента на странице(закрытый аккаунт)
def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence

# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login")
time.sleep(5)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(
    "89961063784")  # логин акаунта
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(
    "DVDazamat100007")  # пароль аккаунта
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()
time.sleep(7)

# считывание файла отфильтровнных пользователей
f = open("filtered_persons_list.txt", "r")
file_list = []
for line in f:
    file_list.append(line)
f.close()

# считывание листа с моими подписками
subscribtions_list = []
f1 = open("my_subscriptions.txt", "r")
for line in f1:
    subscribtions_list.append(line)
f1.close()

j = 0 # номер в терминале
n = 0 # пропущенное число пользователей из за совпадения с subscribetions_list
next_person = 0 #
start_time = time.time() # время  начала цикла

# цикл
for person in file_list:
    z2_likes = z_likes
    # условие для паузы цикла
    if likes >= all_likes:
        time.sleep(60*60*24)
        continue
    if subscribtions >= all_subscriptions:
        time.sleep(60*60*24)
        continue

   # максимальное число подписок в час
    if((time.time() - start_time) <= 60*60) and (hour_sub <= subscribtions):
        time.sleep(60*60 - (time.time() - start_time))
        start_time = time.time()
        subscribtions = 0
        likes = 0

    # максимальное число лайков в час
    if ((time.time() - start_time) <= 60 * 60) and (hour_like <= likes):
        time.sleep(60 * 60 - (time.time() - start_time))
        start_time = time.time()
        subscribtions = 0
        likes = 0
    # обнуление если программа работает больше часа
    if ((time.time() - start_time) >= 60*60):
        start_time = time.time()
        subscribtions = 0
        likes = 0

    # сравнение с массивом подписок
    for line in subscribtions_list:
        next_person = 0
        if person == line:
            next_person = 1
            j += 1
            n += 1
            break
    if next_person == 1:
        continue

    # ввод в терминал номера
    j += 1

    # открытие страницы пользователя
    browser.get(person)
    time.sleep(2)

    # Проверка подписан ли ты на этот аккаунт
    element = "//section/main/div/header/section/div[1]/div[1]/span/span[1]/button"
    if xpath_existence(element) == 1:
        try:
            follow_status = browser.find_element_by_xpath(element).text
        except StaleElementReferenceException:
            xxx = 0
            continue
        if (follow_status == "following") or (follow_status == "Подписки"):
            xxx = 0
            continue

        # количество постов
        element = "//section/main/div/header/section/ul/li[1]/span/span"
        if xpath_existence(element) == 0:
            xxx = 0
            continue
        status = browser.find_element_by_xpath(element).text
        status = re.sub(r'\s', '', status)  # удаление пробелов из числа публикаций
        total_posts = int(status)

        # поиск с публикаций и открытие случайной(ых), лайки
        element = "//a[contains(@href, '/p/')]"
        if xpath_existence(element) == 0:
            xxx = 0
            continue
        posts = browser.find_elements_by_xpath(element)
        i = 0
        for post in posts:
            posts[i] = post.get_attribute('href')
            i += 1

        rand_post_list = [] # количество постов
        if total_posts <= 9:
            for z in range(total_posts):
                rand_post_list.append(z)
        else:
            for z in range(9):
                rand_post_list.append(z)
        while True:
            i = random.choice(rand_post_list) - 1
            browser.get(posts[i])
            rand_post_list.remove(rand_post_list[i]) # удаление повторяющегося элеметна
            time.sleep(1)
            browser.find_element_by_xpath("//section/main/div/div/article/div[2]/section[1]/span[1]/button").click()
            likes += 1
            xxx = 0
            time.sleep(like_time)
            # остановка лайков
            z2_likes -= 1
            if z2_likes == 0:
                break
            elif len(rand_post_list) == 0:
                break

        # 2 подписка на пользователей
        try:
            element = "//section/main/div/div/article/header/div[2]/div[1]/div[2]/button"
            if xpath_existence(element) == 0:
                xxx = 0
            try:
                browser.find_element_by_xpath(element).click()
            except StaleElementReferenceException:
                xxx = 0
                continue
        except ElementClickInterceptedException:
            xxx = 0
            continue

        subscribtions += 1
        time.sleep(0.5)

# завершение работы
browser.quit()

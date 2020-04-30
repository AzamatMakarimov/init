from selenium import webdriver
import time


def one(all_acc, acc, login, password):
    # all_acc количество пользователей которое необходимо нам
    browser = webdriver.Chrome("chromedriver.exe")

    # вход в аккаунт
    browser.get("https://www.instagram.com/accounts/login")
    time.sleep(7)
    browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(login) # логин акаунта
    browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(password) # пароль аккаунта
    browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button/div").click()
    time.sleep(6)

    # выбор аккаунта у которых есть потенциальные подписчики
    browser.get(acc)
    time.sleep(6)
    browser.find_element_by_xpath("//section/main/div/header/section/ul/li[3]/a").click() # открытие списка подписок
    # browser.find_element_by_xpath("//section/main/div/header/section/ul/li[2]/a").click() # открытие списка подписчиков
    time.sleep(5)
    element = browser.find_element_by_xpath("/html/body/div[4]/div/div[2]") # прокручиваемый элемент /html/body/div[3]/div/div[2]

    # плавная прокрутка
    browser.execute_script("arguments[0].scrollTop =arguments[0].scrollHeight/%s" %6, element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop =arguments[0].scrollHeight/%s" %4, element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop =arguments[0].scrollHeight/%s" %3, element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop =arguments[0].scrollHeight/%s" %2, element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop =arguments[0].scrollHeight/%s" %1.4, element)
    time.sleep(0.8)

    pers = set() # массив ссылок на пользователей
    t = 0.7 # пауза после каждой прокрутки
    num_scroll = 0 # количество совершенных прокруток
    p = 0 # коэфицент для ожидания при 2000,4000 ... пользователей

    while len(pers) < all_acc:
        num_scroll += 1
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

        if num_scroll % 15 == 0:
            # сохранение пользователей в массив
            persons = browser.find_elements_by_xpath("//div[@role='dialog']/div[2]/ul/div/li/div/div/div/div/a[@title]")
            for i in range(len(persons)):
                pers.add(str(persons[i].get_attribute('href')))
        time.sleep(3)

        # ожидание
        if (len(pers) > (2000 + 1000 * p)):
            time.sleep(60 * 10)
            p += 1

    # создание файла со списком пользователей
    f = open("persons_list.txt", "w")
    for person in pers:
        f.write(person)
        f.write("\n")
    f.close()

    # закрытие браузера
    browser.quit()

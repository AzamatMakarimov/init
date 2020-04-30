import time
from bottle import route, request,run
import search, filtration, liker, unsubxcriber

# параметры
acc = "https://www.instagram.com/ufa_ufa_rb/" # выбор аккаунта у которых есть потенциальные подписчики
all_acc = 10000 # количество пользователей которое нам нужно
login = "89961063784"
password = "DVDazamat100007"
days = 500 # количество допустимых дней с момента последней публикации
acc_subscriptions = 1200 # количество допустимых подписок у аккаунта
publications = 1 # необходимый минимум публикаций

search.one(all_acc, acc, login, password)
filtration.two(days, acc_subscriptions, publications)
start_time = time.time()
open("liker.py", "r")
time.sleep(60*60)
open("unsubxcriber.py", "r")

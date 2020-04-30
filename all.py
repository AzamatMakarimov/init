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


"""
@route('/instagram', method="POST")
def parameters():
    # параметры
    acc = request.forms.get("acc")  # выбор аккаунта у которых есть потенциальные подписчики
    all_acc = request.forms.get("all_acc")  # количество пользователей которое нам нужно
    login = request.forms.get("login")
    password = request.forms.get("password")
    days = request.forms.get("days")  # количество допустимых дней с момента последней публикации
    acc_subscriptions = request.forms.get("acc_subscriptions")  # количество допустимых подписок у аккаунта
    publications = request.forms.get("publications")  # необходимый минимум публикаций
    like_time = request.forms.get("like_time")  # время между лайками
    all_likes = request.forms.get("all_likes")  # за сутки
    all_subscriptions = request.forms.get("all_subscriptions")  # за сутки
    hour_like = request.forms.get("hour_like")  # максимальное число лайков за час
    hour_sub = request.forms.get("hour_sub")  # максимальное число подписок за час
    z_likes = request.forms.get("z_likes")  # количество лайков которые мы ставим пользователю
    unsub_time = request.forms.get("unsub_time")  # время между отписками (сек)
    max = request.forms.get("max")  # количество отписок, если 0 то все подписки бота
"""


search.one(all_acc, acc, login, password)
filtration.two(days, acc_subscriptions, publications)
start_time = time.time()
open("liker.py", "r")
time.sleep(60*60)
open("unsubxcriber.py", "r")

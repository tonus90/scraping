from pymongo import MongoClient
from pprint import pprint

"""
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
"""
user = 'sergio_gonnzaless' #заданый юзер
client = MongoClient('localhost', 27017)
db = client['instagram']
people = db[user]

followers = people.find({'is_follower': {'$eq': True}})
followings = people.find({'is_following': {'$eq': True}})



def person_print(people): #функция для вывода
    cnt = 0
    for person in people:
        pprint(person)
        cnt+=1
    print(cnt)

person_print(followers)  #выведем его подписчиков
person_print(followings) #выведем его подписки




from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)

db = client['users1403']
# db2 = client['posts'] #можно обращаться к разным базам

users = db.users #тут users уже коллекция
books = db.books
#
# users.insert_one({'name': "Alex"})
#
# result = users.find({})
# for user in result:
#     pprint(user)

users.inser_many()


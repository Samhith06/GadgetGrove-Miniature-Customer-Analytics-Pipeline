import sqlite3
from pymongo import MongoClient

#SQL Connection
conn = sqlite3.connect("shop.db")

with open("setup_sql.sql", "r") as f:
    conn.executescript(f.read())
conn.commit()
conn.close()

#MongoDB Connections
client = MongoClient("mongodb://localhost:27017/")
db = client["GreenField"]
collection = db["reviews"]

print("Connection Sucessfull")
for document in collection.find():
    print(document)
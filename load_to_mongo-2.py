from xmlrpc import client
from pymongo import MongoClient
import json
import os


MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://goitlearn:@cluster0.ebwl04i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(MONGO_URI)
db = client["quotes_db"]


with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

with open("authors.json", "r", encoding="utf-8") as f:
    authors = json.load(f)
db.quotes.delete_many({})
db.authors.delete_many({})


print("✅ Данные успешно загружены в MongoDB Atlas")


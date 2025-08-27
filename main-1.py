import os
from pymongo import MongoClient
from bson.objectid import ObjectId


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)
db = client["cats_db"]
collection = db["cats"]




###Create###
def create_cat(name, age, features):
    try:
        cat = {"name":name, "age":age, "features":features}
        result = collection.insert_one(cat)
        print (f"Додано кота з _id: {result.inserted_id}")
    except Exception as e:
        print("Помилка при додаванні", e)





###Read###
def show_all_cats():
    try:
        for cat in collection.find():
            print (cat)
    except Exception as e :
            print("Помилка при читанні", e)
def get_cat_by_name(name):
    try:
        cat = collection.find_one({"name":name})
        if cat :
            print(cat)
        else:
            print("Немає кіта з таким ім'ям")
    except Exception as e:
        print("Помилка при пошуку",e)



###Update###

def update_age_by_name(name,new_age):
    try:
        result = collection.update_one({"name":name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print("Вік оновленно")
        else: 
            print("Немає кіта з таким ім'ям")
    except Exception as e:
        print("Помилка при оновленні",e)



def add_feature_by_name(name, feature):
    try:
        result = collection.update_one({"name": name},{"$push": {"features": feature}})
        if result.matched_count:
            print("Опис додано")
        else:
            print("Немає кіта з таким ім'ям")
    except Exception as e:
        print("Помилка при додаванні опису", e)


###Delete###

def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name":name})
        if result.deleted_count:
            print("Кіта видаленно")
        else:
            print("Немає кіта з таким ім'ям")
    except Exception as e:
        print("Помилка при видаленні",e)

def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Записів видаленно: {result.deleted_count}")
    except Exception as e:
        print("Помилка при масовому видаленні",e)


####MAIN####
if __name__ == "__main__":
    while True:
        print("\n=== МЕНЮ ===")
        print("\n1. Додати кота")
        print("\n2. Показати всіх котів")
        print("\n3. Знайти кота за ім'ям")
        print("\n4. Оновити вік кота")
        print("\n5. Додати характеристику коту")
        print("\n6. Видалити кота за ім'ям")
        print("\n7. Видалити всіх котів")
        print("\n0. Вийти")

        choice = input("Оберіть дію: ")

        if choice == "1":
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики через кому: ").split(",")
            features = [f.strip() for f in features]
            create_cat(name, age, features)

        elif choice == "2":
            show_all_cats()

        elif choice == "3":
            name = input("Введіть ім'я кота: ")
            get_cat_by_name(name)

        elif choice == "4":
            name = input("Введіть ім'я кота: ")
            new_age = int(input("Введіть новий вік: "))
            update_age_by_name(name, new_age)

        elif choice == "5":
            name = input("Введіть ім'я кота: ")
            feature = input("Введіть нову характеристику: ")
            add_feature_by_name(name, feature)

        elif choice == "6":
            name = input("Введіть ім'я кота: ")
            delete_cat_by_name(name)

        elif choice == "7":
            deltete_all_cats()

        elif choice == "0":
            print("Вихід з програми.")
            break

        else:
            print("Щось пішло не так")

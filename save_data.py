import json
from pymongo import MongoClient

def save_data_to_mongodb():
    with open("final_data.json", "r") as final_data_file:
        final_data = json.load(final_data_file)

    # client = MongoClient("mongodb://localhost:27017")
    client = MongoClient("mongodb://host.docker.internal:27017")
    db = client["tayfun_karakavuz"]
    collection = db["cities"]

    for city_id, data in final_data.items():
        db.cities.insert_one({city_id: data})

    client.close()

    print(f"Data has been saved to the 'tayfun_karakavuz' database in MongoDB.")


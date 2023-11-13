import json
from unidecode import unidecode

def filter_cities_and_save_data():
    JSON_FILE_PATH = "assets/weathercom/weathercom_data.json"
    with open('cities.json', 'r') as cities_file:
        cities_data = json.load(cities_file)
        city_mapping = {unidecode(city["name"]).lower(): int(city["id"]) for city in cities_data}


    with open(JSON_FILE_PATH, 'r') as weathercom_file:
        weathercom_data = json.load(weathercom_file)


    updated_weathercom_data = {}
    updated_city_count = 0

    for city_name, city_data in weathercom_data.items():
        lowercase_city_name = unidecode(city_name).lower()
        city_id = city_mapping.get(lowercase_city_name)
        
        if city_id is not None:
            updated_weathercom_data[city_id] = city_data
            updated_city_count += 1

    with open("assets/weathercom/weathercom_data.json", 'w') as updated_weathercom_file:
        json.dump(updated_weathercom_data, updated_weathercom_file, indent=4)

    
    print(f"Updated {updated_city_count} cities.")
    return updated_city_count
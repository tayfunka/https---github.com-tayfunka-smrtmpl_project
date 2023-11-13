import json

def filter_cities_and_save_data():
    JSON_FILE_PATH = "assets/havadurumux/havadurumux_data.json"
    with open('cities.json', 'r') as cities_file:
        cities_data = json.load(cities_file)
        city_mapping = {city["name"].lower(): int(city["id"]) for city in cities_data}


    with open(JSON_FILE_PATH, 'r') as havadurumux_file:
        havadurumux_data = json.load(havadurumux_file)


    updated_havadurumux_data = {}
    count = 0

    for city_name, city_data in havadurumux_data.items():
        lowercase_city_name = city_name.lower()
        city_id = city_mapping.get(lowercase_city_name)
        
        if city_id is not None:
            updated_havadurumux_data[city_id] = city_data
            count += 1

    with open('assets/havadurumux/havadurumux_data.json', 'w') as updated_havadurumux_file:
        json.dump(updated_havadurumux_data, updated_havadurumux_file, indent=4)

    print(f"Updated {count} cities.")
    return count

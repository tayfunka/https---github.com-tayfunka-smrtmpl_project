import json

JSON_FILE_PATH = "assets/metoffice/metoffice_data.json"

def filter_cities_and_save_data():
    with open('cities.json', 'r') as cities_file:
        cities_data = json.load(cities_file)
        city_mapping = {city["name"].lower(): city["id"] for city in cities_data}

    with open(JSON_FILE_PATH, 'r') as metoffice_file:
        metoffice_data = json.load(metoffice_file)

    updated_metoffice_data = {}
    unmatched_cities = {}
    count = 0
    for city_name, city_data in metoffice_data.items():
        lowercase_city_name = city_name.lower()
        city = city_mapping.get(lowercase_city_name)
        if city is not None:
            count += 1
            updated_metoffice_data[city] = city_data
        else:
            unmatched_cities[city_name] = city_data

    with open('assets/metoffice/metoffice_data.json', 'w') as updated_metoffice_file:
        json.dump(updated_metoffice_data, updated_metoffice_file, indent=4)

    with open('assets/metoffice/unmatched_cities.json', 'w') as unmatched_cities_file:
        json.dump(unmatched_cities, unmatched_cities_file, indent=4)

    return count

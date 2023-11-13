import json

def merge_data():
    with open("assets/metoffice/metoffice_data.json", "r") as metoffice_file:
        metoffice_data = json.load(metoffice_file)

    with open("assets/havadurumux/havadurumux_data.json", "r") as havadurumux_file:
        havadurumux_data = json.load(havadurumux_file)

    with open("assets/weathercom/weathercom_data.json", "r") as weathercom_file:
        weathercom_data = json.load(weathercom_file)

    final_data = {}
    city_count = 0

    for city in weathercom_data:
        city_count += 1
        final_data[city] = {}

        for date in weathercom_data[city]:
            final_data[city][date] = {"weather": {}}

            if city in metoffice_data and date in metoffice_data[city]:
                final_data[city][date]["weather"]["metoffice"] = metoffice_data[city][date]["weather"]["metoffice"]

            if city in havadurumux_data and date in havadurumux_data[city]:
                final_data[city][date]["weather"]["havadurumux"] = havadurumux_data[city][date]["weather"]["havadurumux"]

            final_data[city][date]["weather"]["weathercom"] = weathercom_data[city][date]["weather"]["weathercom"]

    # Save the final_data to final_data.json
    with open("final_data.json", "w") as final_data_file:
        json.dump(final_data, final_data_file, indent=4)

    print(f"final_data.json has been created with data for {city_count} cities.")

from requests_html import HTML
from requests_html import AsyncHTMLSession
import asyncio
import json
import time
from datetime import datetime, timedelta
from assets.metoffice.metoffice_filter_cities import filter_cities_and_save_data

asession = AsyncHTMLSession()

MAX_RETRIES = 3
RETRY_DELAY = 5
JSON_FILE_PATH = "assets/metoffice/metoffice_data.json"


async def get_metoffice_city_list():
    r = await asession.get("https://www.metoffice.gov.uk/weather/world/turkey/list")
    metoffice_url_list = [
        item for item in r.html.links if item.startswith("/weather/forecast/s")
    ]
    return metoffice_url_list

metoffice_url_list = asession.run(get_metoffice_city_list)
result = metoffice_url_list[0]

base_url = "https://www.metoffice.gov.uk/"


async def fetch_url_with_retry(url, max_retries, retry_delay):
    for _ in range(max_retries):
        try:
            r = await asession.get(url)
            r.raise_for_status()
            return r
        except Exception as e:
            print(f"Error: {e}")
            print(f"Retrying in {retry_delay} seconds...")
            await asyncio.sleep(retry_delay)
    return None

async def get_metoffice_data():
    try:
        with open(JSON_FILE_PATH, "r") as json_file:
            city_data = json.load(json_file)
    except FileNotFoundError:
        city_data = {}

    current_date = datetime.now()
    start_date = current_date + timedelta(days=1)

    for city_url in result:
        response = await fetch_url_with_retry(
            base_url + city_url, MAX_RETRIES, RETRY_DELAY
        )

        if response is not None:
            html_r = HTML(html=response.text)

            city_name_element = html_r.find("#location-search-input", first=True)
            city_name = city_name_element.attrs.get("value").split(" (")[0]
            # print(f"Data fetched for the city: {city_name}")
            city_data.setdefault(city_name, {})

            for i in range(1, 6):
                date = (start_date + timedelta(days=i - 1)).strftime("%Y-%m-%d")

                high_element = html_r.find(f"#tabDay{i} .tab-temp-high", first=True)
                low_element = html_r.find(f"#tabDay{i} .tab-temp-low", first=True)

                high = float(high_element.attrs.get("data-value"))
                low = float(low_element.attrs.get("data-value"))

                city_data[city_name][date] = {
                    "weather": {"metoffice": {"high": high, "low": low}}
                }

    return city_data


async def main():
    start_time = time.time()
    data = await get_metoffice_data()

    with open(JSON_FILE_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)

    num_cities = len(data)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Data has been updated and written to " + JSON_FILE_PATH)
    print(f"Total number of cities saved in the metoffice_data.json: {num_cities}")
    print(f" 'metoffice: ' Elapsed time: {elapsed_time:.2f} seconds")

    count = filter_cities_and_save_data()
    print(f" 'metoffice: Number of cities matched and saved: {count}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

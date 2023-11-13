from requests_html import HTML
from requests_html import AsyncHTMLSession
import asyncio
import json
import time
from datetime import datetime, timedelta
from assets.havadurumux.havadurumux_filter_cities import filter_cities_and_save_data
asession = AsyncHTMLSession()

MAX_RETRIES = 3
RETRY_DELAY = 5
JSON_FILE_PATH = "assets/havadurumux/havadurumux_data.json"


async def get_havadurumux_city_list():
    r = await asession.get("https://www.havadurumux.net/tum-sehirler/")
    havadurumux_url_list = [
        item for item in r.html.links if item.endswith("-hava-durumu/")
    ]
    return havadurumux_url_list

havadurumux_url_list = asession.run(get_havadurumux_city_list)
result = havadurumux_url_list[0]

base_url = "https://www.havadurumux.net/"


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


async def get_havadurumux_data():
    try:
        with open(JSON_FILE_PATH, "r") as json_file:
            city_data = json.load(json_file)
    except FileNotFoundError:
        city_data = {}

    website_name = "havadurumux"


    current_date = datetime.now()
    start_date = current_date + timedelta(days=1)

    for city_url in result:
        city_name = city_url.split("/")[-2].replace("-hava-durumu", "")

        # print(f"Fetching data for city: {city_name}")

        response = await fetch_url_with_retry(city_url, MAX_RETRIES, RETRY_DELAY)

        if response is not None:
            html_r = HTML(html=response.text)

            table_rows = html_r.find("tbody tr")[1:6]

            city_data.setdefault(city_name, {})

            for i, row in enumerate(table_rows):
                date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

                high_temperature = float(row.find("td")[2].text.replace("°", ""))
                low_temperature = float(row.find("td")[3].text.replace("°", ""))

                city_data[city_name][date] = {
                    "weather": {
                        website_name: {"high": high_temperature, "low": low_temperature}
                    }
                }

    return city_data


async def main():
    start_time = time.time()
    data = await get_havadurumux_data()

    with open(JSON_FILE_PATH, "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    num_cities = len(data)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Data has been updated and written to " + JSON_FILE_PATH)
    print(f"Total number of cities saved in the JSON file: {num_cities}")
    print(f"'havadurumux: ' Elapsed time: {elapsed_time:.2f} seconds")

    count = filter_cities_and_save_data()
    print(f"'havadurumux: 'Number of cities matched and saved: {count}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
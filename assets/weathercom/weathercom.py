from requests_html import HTML
from requests_html import AsyncHTMLSession
import asyncio
import json
import time
from datetime import datetime, timedelta
from assets.weathercom.weathercom_filter_cities import filter_cities_and_save_data
current_date = datetime.now()
tomorrow = current_date + timedelta(days=1)

asession = AsyncHTMLSession()

loop = asyncio.get_event_loop()
MAX_RETRIES = 3
RETRY_DELAY = 5
JSON_FILE_PATH = "assets/weathercom/weathercom_data.json"

base_url = "https://weather.com/weather/tenday/l/"


def get_weathercom_city_ids():
    city_ids = []

    with open("assets/weathercom/city_ids.json", "r") as file:
        city_data = json.load(file)

        for city in city_data:
            city_ids.append(city["city_id"])

    return city_ids


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


async def fahrenheit_to_celsius(fahrenheit):
    # Convert Fahrenheit to Celsius and round to one decimal place
    celsius = (fahrenheit - 32) * 5/9
    return round(celsius, 1)

async def get_weathercom_data():
    try:
        with open(JSON_FILE_PATH, "r") as json_file:
            city_data = json.load(json_file)
    except FileNotFoundError:
        city_data = {}

    for city_url in result:
        response = await fetch_url_with_retry(
            base_url + city_url, MAX_RETRIES, RETRY_DELAY
        )

        if response is not None:
            html_r = HTML(html=response.text)
            city_name_element = html_r.find(
                "span.LocationPageTitle--PresentationName--1AMA6", first=True
            )
            city_name = city_name_element.text.split(",")[0].strip().replace("Province", "").strip()

            # Handle specific city name replacements
            if city_name == "Handırı":
                city_name = "Çankırı"
            elif city_name == "Marash":
                city_name = "Kahramanmaraş"

            # print(f"Data fetched for the city: {city_name}")

            day_details = html_r.find("details.DaypartDetails--DayPartDetail--2XOOV")
            city_data.setdefault(city_name, {})

            for i, day in enumerate(day_details[1:6]):

                date = tomorrow + timedelta(days=i)

                high_temp_element = day.find(
                    "span.DetailsSummary--highTempValue--3PjlX", first=True
                )
                low_temp_element = day.find(
                    "span.DetailsSummary--lowTempValue--2tesQ", first=True
                )
                high_temp_str = high_temp_element.text.strip().replace("°", "")
                low_temp_str = low_temp_element.text.strip().replace("°", "")
                high_temp_fahrenheit = float(high_temp_str)
                low_temp_fahrenheit = float(low_temp_str)

                high_temp_celsius = await fahrenheit_to_celsius(high_temp_fahrenheit)
                low_temp_celsius = await fahrenheit_to_celsius(low_temp_fahrenheit)

                city_data[city_name][date.strftime("%Y-%m-%d")] = {"weather": {"weathercom": {
                    "high": high_temp_celsius,
                    "low": low_temp_celsius
                }
            }
    }
    
    return city_data
    

city_ids = get_weathercom_city_ids()
result = city_ids
    

async def main():
    start_time = time.time()
    data = await get_weathercom_data()
    with open(JSON_FILE_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    num_cities = len(data)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Data has been updated and written to " + JSON_FILE_PATH)
    print(f"Total number of cities saved in the weathercom_data.json: {num_cities}")
    print(f" 'weathercom: ' Elapsed time: {elapsed_time:.2f} seconds")

    count = filter_cities_and_save_data()
    print(f" 'weathercom: ' Number of cities matched and saved: {count}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

url = "https://weather.com/tr-TR/weather/tenday/l/91c4e7f67daaedeea9bf761b82affbf27025e2f9bd62b2978d21897cf038566e"


def read_city_names(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return {city["id"]: city["name"] for city in data}


def save_city_ids(data):
    with open("city_ids.json", "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def scraper(url):
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    truste_consent_button = driver.find_element(By.ID, "truste-consent-button")
    truste_consent_button.click()
    time.sleep(5)
    search_box = driver.find_element(By.ID, "LocationSearch_input")

    city_names = read_city_names("assets/cities.json")

    city_ids = []

    for city_id, city_name in city_names.items():
        search_box.clear()
        search_box.send_keys(city_name)
        time.sleep(3)
        page_source = driver.page_source
        substring = "LocationSearch_listbox-"
        index = page_source.find(substring)

        if index != -1:
            index += len(substring)
            extracted_string = page_source[index : index + 64]
            city_ids.append({"city_name": city_name, "city_id": extracted_string})
        else:
            print(f"Substring '{substring}' not found for city: {city_name}")
            city_ids.append(None)  # Or handle this case as needed
    
    driver.close()
    return city_ids


city_ids = scraper(url)
read_city_names("assets/cities.json")
save_city_ids(city_ids)

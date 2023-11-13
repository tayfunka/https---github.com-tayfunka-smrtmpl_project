import assets.havadurumux.havadurumux as havadurumux
import assets.metoffice.metoffice as metoffice
import assets.weathercom.weathercom as weathercom
from requests_html import AsyncHTMLSession
import merge_data
import save_data
import time

def run():
    asession = AsyncHTMLSession()
    asession.run(havadurumux.main, metoffice.main, weathercom.main)

def save():
    merge_data.merge_data()
    save_data.save_data_to_mongodb()

if __name__ == "__main__":
    start_time = time.time()
    run()
    save()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time:.2f} seconds")
import requests
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")  


city = input("Enter city name: ")

base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

weather_data = requests.get(base_url)
pprint(weather_data.json())
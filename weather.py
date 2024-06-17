import requests
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

def fetch_country_codes():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    country_codes = {country["cca2"]: country["name"]["common"] for country in data}
    return country_codes

def get_weather(api_key, city, country):
    encoded_city = urllib.parse.quote(city.strip())
    url = f"http://api.openweathermap.org/data/2.5/weather?q={encoded_city},{country.strip()}&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def print_weather(data):
    city = data["name"]
    country = data["sys"]["country"]
    temp_celsius = data["main"]["temp"] - 273.15  # Convert temperature from Kelvin to Celsius
    temp_fahrenheit = (temp_celsius * 9/5) + 32  # Convert Celsius to Fahrenheit
    weather_description = data["weather"][0]["description"]
    print(f"Weather in {city}, {country}:")
    print(f"Temperature: {temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F")
    print(f"Description: {weather_description}")

def main():
    import argparse

    # Fetch country codes
    country_codes = fetch_country_codes()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Get the current weather for a city")
    parser.add_argument("city", type=str, help="The name of the city to get the weather for")
    parser.add_argument("country", type=str, help="The country code of the city to get the weather for")
    args = parser.parse_args()

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please set the OPENWEATHERMAP_API_KEY environment variable.")

    city = args.city.strip()
    country = args.country.strip()

    if country not in country_codes:
        raise ValueError(f"Invalid country code: {country}. Please provide a valid ISO 3166-1 alpha-2 country code.")

    weather_data = get_weather(api_key, city, country)
    print_weather(weather_data)

if __name__ == "__main__":
    main()

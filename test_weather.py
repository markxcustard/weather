import pytest
import requests
from weather import fetch_country_codes, get_weather, print_weather

@pytest.fixture
def mock_country_codes(monkeypatch):
    mock_data = {
        "GB": "United Kingdom",
        "US": "United States",
        # Add more mock country codes as needed
    }

    def mock_fetch_country_codes():
        return mock_data

    monkeypatch.setattr('weather.fetch_country_codes', mock_fetch_country_codes)
    return mock_data

@pytest.fixture
def mock_weather_data():
    return {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 280.32},
        "weather": [{"description": "clear sky"}]
    }

def test_fetch_country_codes(requests_mock):
    requests_mock.get("https://restcountries.com/v3.1/all", json=[
        {"cca2": "GB", "name": {"common": "United Kingdom"}},
        {"cca2": "US", "name": {"common": "United States"}},
    ])
    country_codes = fetch_country_codes()
    assert country_codes["GB"] == "United Kingdom"
    assert country_codes["US"] == "United States"

def test_get_weather(requests_mock, mock_weather_data):
    api_key = "fake_api_key"
    city = "London"
    country = "GB"
    requests_mock.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}", json=mock_weather_data)
    weather_data = get_weather(api_key, city, country)
    assert weather_data["name"] == "London"
    assert weather_data["sys"]["country"] == "GB"

def test_print_weather(capfd, mock_weather_data):
    print_weather(mock_weather_data)
    out, err = capfd.readouterr()
    assert "Weather in London, GB:" in out
    assert "Temperature: 7.17°C / 44.91°F" in out  # 280.32K - 273.15 = 7.17°C; (7.17 * 9/5) + 32 = 44.91°F
    assert "Description: clear sky" in out

# Negative Test: Invalid API Key
def test_invalid_api_key(requests_mock):
    api_key = "invalid_api_key"
    city = "London"
    country = "GB"
    requests_mock.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}", status_code=401)
    with pytest.raises(requests.exceptions.HTTPError):
        get_weather(api_key, city, country)

# Boundary Test: Empty City Name
def test_empty_city_name(requests_mock):
    api_key = "fake_api_key"
    city = ""
    country = "GB"
    requests_mock.get(f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}", status_code=400)
    with pytest.raises(requests.exceptions.HTTPError):
        get_weather(api_key, city, country)

# Boundary Test: Extremely High Temperature
@pytest.fixture
def mock_extreme_weather_data():
    return {
        "name": "Death Valley",
        "sys": {"country": "US"},
        "main": {"temp": 373.15},  # 100°C / 212°F
        "weather": [{"description": "extreme heat"}]
    }

def test_print_extreme_weather(capfd, mock_extreme_weather_data):
    print_weather(mock_extreme_weather_data)
    out, err = capfd.readouterr()
    assert "Weather in Death Valley, US:" in out
    assert "Temperature: 100.00°C / 212.00°F" in out
    assert "Description: extreme heat" in out

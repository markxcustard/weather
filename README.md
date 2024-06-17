# Weather API Client

This project is a simple Python application that fetches and displays weather information for a specified city and country using the OpenWeatherMap API. The application includes both Celsius and Fahrenheit temperature conversions and provides comprehensive unit tests using `pytest`.

## Features

- Fetches current weather data for a specified city and country.
- Converts temperature from Kelvin to Celsius and Fahrenheit.
- Handles invalid API keys, empty city names, and other edge cases.
- Provides detailed unit tests including negative and boundary tests.

## Prerequisites

- Python 3.7+
- `pip` (Python package installer)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/weather-api-client.git
    cd weather-api-client
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root directory and add your OpenWeatherMap API key:

    ```env
    OPENWEATHERMAP_API_KEY=your_api_key_here
    ```

## Usage

To fetch and display weather information for a city, run the script with the city name and country code as arguments:

```sh
python weather.py <city> <country_code>

Example: python weather.py London GB


Testing
This project uses pytest for unit testing. The tests include:

Fetching country codes.
Fetching weather data.
Printing weather data with temperature conversions.
Negative tests for invalid API keys.
Boundary tests for empty city names and extreme temperatures.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

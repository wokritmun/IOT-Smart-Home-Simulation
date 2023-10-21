import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather_data(latitude=25, longitude=13):
    """
    Fetches weather data for the given latitude and longitude.

    Args:
        latitude (float, optional): Latitude value. Defaults to 25 (for Sahara Desert).
        longitude (float, optional): Longitude value. Defaults to 13 (for Sahara Desert).

    Returns:
        dict: A dictionary containing the weather data.
    """
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,rain,weathercode,cloudcover,visibility,evapotranspiration'
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Raises exception for HTTP errors

    return response.json()

if __name__ == "__main__":
    # Test the function
    data = get_weather_data()
    print(data)

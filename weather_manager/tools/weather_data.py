####################################################################################################
####################  FrankyX | Weather Manager - Tools         ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################
import requests
import json
import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError

logger = logging.getLogger(__name__)

def get_coordinates_for_location_string(location_string: str) -> str:
    """
    Geocodes a location string (e.g., city, zip code) to latitude and longitude.
    Returns a JSON string with 'latitude', 'longitude', and 'full_address', or an error.
    """
    logger.info(f"Geocoding location: '{location_string}'")
    
    # To improve accuracy, especially for US zip codes, append ", USA" if it's not already present
    if "usa" not in location_string.lower() and "united states" not in location_string.lower():
        geocoding_query = f"{location_string}, USA"
    else:
        geocoding_query = location_string
        
    logger.info(f"Using geocoding query: '{geocoding_query}'")
    geolocator = Nominatim(user_agent="franky_x_weather_agent_v1_0_your_app")
    try:
        location = geolocator.geocode(geocoding_query, timeout=10)
        if location:
            result = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "full_address": location.address
            }
            logger.info(f"Geocoded successfully: {result}")
            return json.dumps(result)
        else:
            logger.warning(f"Location '{location_string}' not found.")
            return json.dumps({"error": f"I could not find the location '{location_string}'. Please be more specific."})
    except GeocoderTimedOut:
        logger.error("Geocoding service timed out.")
        return json.dumps({"error": "The location service timed out. Please try again in a moment."})
    except Exception as e:
        logger.error(f"An unexpected error occurred during geocoding: {e}", exc_info=True)
        return json.dumps({"error": "An unexpected error occurred while trying to find the location."})

def get_weather_for_location(latitude: float, longitude: float, timezone: str) -> str:
    """
    Fetches detailed weather data from Open-Meteo for a given latitude, longitude, and timezone.
    Returns a JSON string with detailed weather data or an error message.
    """
    logger.info(f"Fetching weather for Lat: {latitude}, Lon: {longitude}, Timezone: {timezone}")
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,pressure_msl",
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m,wind_gusts_10m,uv_index",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max",
        "timezone": timezone,
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        weather_data = response.json()
        logger.info("Weather data fetched successfully.")
        return json.dumps(weather_data)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error fetching weather: {http_err}", exc_info=True)
        return json.dumps({"error": f"The weather service returned an HTTP error: {http_err}"})
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error fetching weather: {req_err}", exc_info=True)
        return json.dumps({"error": f"A network error occurred: {req_err}"})
####################################################################################################
####################  FrankyX | Weather Manager - Tools         ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################
import requests
import json
import logging
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
# from timezonefinder import TimezoneFinder # Optional: for more precise timezone

# Optional: Initialize timezone finder if you want more precise timezone
# tf = TimezoneFinder()

logger = logging.getLogger(__name__)

def get_coordinates_for_location_string(location_string: str) -> str:
    """
    Geocodes a location string (e.g., city name, address, zip code) to latitude and longitude.
    Returns a JSON string with 'latitude', 'longitude', and 'full_address',
    or an error message if not found or an error occurs.
    The agent should use these coordinates with the 'get_weather_for_location' tool.
    """
    logger.info(f"Geocoding location: {location_string}")
    # It's good practice to set a unique user_agent for Nominatim
    geolocator = Nominatim(user_agent="franky_x_weather_agent_v1_0_your_app") 
    try:
        location = geolocator.geocode(location_string, timeout=10)
        if location:
            result = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "full_address": location.address
            }
            logger.info(f"Geocoded successfully: {result}")
            return json.dumps(result)
        else:
            logger.warning(f"Location '{location_string}' not found by geocoder.")
            return json.dumps({"error": f"Location '{location_string}' not found."})
    except GeocoderTimedOut:
        logger.error(f"Geocoding service timed out for '{location_string}'.")
        return json.dumps({"error": "Geocoding service timed out. Please try again later."})
    except GeocoderUnavailable:
        logger.error(f"Geocoding service unavailable for '{location_string}'.")
        return json.dumps({"error": "Geocoding service currently unavailable. Please try again later."})
    except GeocoderServiceError as e:
        logger.error(f"Geocoding service error for '{location_string}': {e}", exc_info=True)
        return json.dumps({"error": f"Geocoding service error: {str(e)}. Please check location or try again."})
    except Exception as e:
        logger.error(f"An unexpected error occurred during geocoding for '{location_string}': {e}", exc_info=True)
        return json.dumps({"error": f"An unexpected error occurred during geocoding: {str(e)}"})

def get_weather_for_location(latitude: float, longitude: float, timezone: str = "auto") -> str:
    """
    Fetches weather data from Open-Meteo for a given latitude and longitude.
    'timezone' can be specified (e.g., 'America/Chicago') or set to 'auto' for Open-Meteo to determine.
    Returns a JSON string containing the weather data or an error message.
    The agent should interpret this data to answer user queries.
    """
    logger.info(f"Fetching weather for Lat: {latitude}, Lon: {longitude}, Timezone: {timezone}")
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": "temperature_2m,relativehumidity_2m,precipitation_probability,weathercode,windspeed_10m,winddirection_10m",
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max",
        "timezone": timezone,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        weather_data = response.json()
        logger.info("Weather data fetched successfully.")
        return json.dumps(weather_data)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred while fetching weather: {http_err}", exc_info=True)
        return json.dumps({"error": f"Weather service returned an HTTP error: {str(http_err)}"})
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error occurred while fetching weather: {conn_err}", exc_info=True)
        return json.dumps({"error": "Could not connect to weather service. Please check network connection."})
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout occurred while fetching weather: {timeout_err}", exc_info=True)
        return json.dumps({"error": "Request to weather service timed out. Please try again later."})
    except requests.exceptions.TooManyRedirects as redir_err:
        logger.error(f"Too many redirects occurred while fetching weather: {redir_err}", exc_info=True)
        return json.dumps({"error": "Too many redirects encountered when contacting weather service."})
    except requests.exceptions.RequestException as req_err: # More general request exception
        logger.error(f"Request error occurred while fetching weather: {req_err}", exc_info=True)
        return json.dumps({"error": f"An error occurred during request to weather service: {str(req_err)}"})
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON weather response.", exc_info=True)
        return json.dumps({"error": "Failed to decode weather service response. The service might be temporarily unavailable or returned invalid data."})
    except Exception as e:
        logger.error(f"An unexpected error occurred fetching weather: {e}", exc_info=True)
        return json.dumps({"error": f"An unexpected error occurred while fetching weather data: {str(e)}"})

# Example usage (for testing the tools directly)
if __name__ == "__main__":
    # Basic logging configuration for the test script execution
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logger.info("Testing Geocoding Tool...")
    # Test with a city/state
    geo_info_str = get_coordinates_for_location_string("Gardner, Kansas")
    logger.info(f"Geocoding Response (Gardner, Kansas): {geo_info_str}")
    
    # Test with a zip code
    # geo_info_str_zip = get_coordinates_for_location_string("66030") # Zip for Gardner, KS
    # logger.info(f"Geocoding Response (66030): {geo_info_str_zip}")

    geo_data = json.loads(geo_info_str)
    if "latitude" in geo_data:
        lat = geo_data["latitude"]
        lon = geo_data["longitude"]
        
        # Optional: More precise timezone detection
        # tz_finder = TimezoneFinder()
        # tz_str = tz_finder.timezone_at(lng=lon, lat=lat)
        # if not tz_str:
        #     logger.info(f"Timezone not found for {lat},{lon}, using 'auto'")
        #     tz_str = "auto"
        # else:
        # logger.info(f"Detected Timezone: {tz_str}")
        
        logger.info("\nTesting Weather Fetching Tool...")
        # weather_info_str = get_weather_for_location(lat, lon, timezone=tz_str)
        weather_info_str = get_weather_for_location(lat, lon) # Using "auto" timezone as default
        logger.info(f"Weather Response: {weather_info_str}")

        # Example of how the LLM might get the data (it would get the string, then parse it)
        # if weather_info_str:
        #     weather_data_parsed = json.loads(weather_info_str)
        #     if "error" not in weather_data_parsed:
        #         logger.info(f"\nSample Current Weather Temp: {weather_data_parsed.get('current_weather', {}).get('temperature')}")
    else:
        logger.warning("Could not geocode the primary location to test weather tool.")
import unittest
import json
from unittest.mock import patch, Mock

# Attempt to import from the correct location
# This assumes the tests will be run from a context where FrankyX is a package
try:
    from FrankyX.weather_manager.tools.weather_data import get_coordinates_for_location_string, get_weather_for_location
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
    import requests
except ImportError:
    # Fallback for cases where the context might be different (e.g. running script directly)
    # This might be needed if PYTHONPATH is not set up for FrankyX as a top-level package
    # For the sandbox, the first try block should ideally work.
    import sys
    import os
    # Add the parent directory of FrankyX to sys.path
    # This is a bit of a hack for local running, ideally PYTHONPATH is configured
    current_dir = os.path.dirname(os.path.abspath(__file__)) # FrankyX/weather_manager/tests
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir))) # Should be directory containing FrankyX
    sys.path.insert(0, project_root) 
    
    from FrankyX.weather_manager.tools.weather_data import get_coordinates_for_location_string, get_weather_for_location
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
    import requests


class TestWeatherDataTools(unittest.TestCase):

    # Tests for get_coordinates_for_location_string
    @patch('FrankyX.weather_manager.tools.weather_data.Nominatim')
    def test_get_coordinates_success(self, MockNominatim):
        mock_geolocator_instance = MockNominatim.return_value
        mock_location = Mock()
        mock_location.latitude = 38.8951
        mock_location.longitude = -77.0364
        mock_location.address = "Washington, D.C., USA"
        mock_geolocator_instance.geocode.return_value = mock_location

        result_str = get_coordinates_for_location_string("Washington D.C.")
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)

        self.assertIn("latitude", result_json)
        self.assertIn("longitude", result_json)
        self.assertIn("full_address", result_json)
        self.assertEqual(result_json["latitude"], 38.8951)
        self.assertEqual(result_json["longitude"], -77.0364)
        self.assertEqual(result_json["full_address"], "Washington, D.C., USA")
        MockNominatim.assert_called_once_with(user_agent="franky_x_weather_agent_v1_0_your_app")
        mock_geolocator_instance.geocode.assert_called_once_with("Washington D.C.", timeout=10)

    @patch('FrankyX.weather_manager.tools.weather_data.Nominatim')
    def test_get_coordinates_not_found(self, MockNominatim):
        mock_geolocator_instance = MockNominatim.return_value
        mock_geolocator_instance.geocode.return_value = None

        result_str = get_coordinates_for_location_string("InvalidLocation123")
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)

        self.assertIn("error", result_json)
        self.assertEqual(result_json["error"], "Location 'InvalidLocation123' not found.")

    @patch('FrankyX.weather_manager.tools.weather_data.Nominatim')
    def test_get_coordinates_geocoder_timeout(self, MockNominatim):
        mock_geolocator_instance = MockNominatim.return_value
        mock_geolocator_instance.geocode.side_effect = GeocoderTimedOut("Service timed out")

        result_str = get_coordinates_for_location_string("A City")
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertEqual(result_json["error"], "Geocoding service timed out. Please try again later.")

    @patch('FrankyX.weather_manager.tools.weather_data.Nominatim')
    def test_get_coordinates_geocoder_unavailable(self, MockNominatim):
        mock_geolocator_instance = MockNominatim.return_value
        mock_geolocator_instance.geocode.side_effect = GeocoderUnavailable("Service unavailable")

        result_str = get_coordinates_for_location_string("Another City")
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertEqual(result_json["error"], "Geocoding service currently unavailable. Please try again later.")

    @patch('FrankyX.weather_manager.tools.weather_data.Nominatim')
    def test_get_coordinates_geocoder_service_error(self, MockNominatim):
        mock_geolocator_instance = MockNominatim.return_value
        mock_geolocator_instance.geocode.side_effect = GeocoderServiceError("Service error")

        result_str = get_coordinates_for_location_string("Some Place")
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertTrue("Geocoding service error" in result_json["error"])


    # Tests for get_weather_for_location
    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_success(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {"current_weather": {"temperature": 25}, "daily": {}}
        mock_response.raise_for_status = Mock() # Does nothing for success
        mock_requests_get.return_value = mock_response

        result_str = get_weather_for_location(38.8951, -77.0364)
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)

        self.assertIn("current_weather", result_json)
        self.assertEqual(result_json["current_weather"]["temperature"], 25)
        mock_requests_get.assert_called_once()
        # We could also assert the URL and params if needed, but this is a good start

    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_http_error(self, mock_requests_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_requests_get.return_value = mock_response

        result_str = get_weather_for_location(10, 10)
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertTrue("Weather service returned an HTTP error" in result_json["error"])

    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_connection_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result_str = get_weather_for_location(20, 20)
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertEqual(result_json["error"], "Could not connect to weather service. Please check network connection.")
        
    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_timeout_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.Timeout("Request timed out")

        result_str = get_weather_for_location(30, 30)
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertEqual(result_json["error"], "Request to weather service timed out. Please try again later.")

    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_too_many_redirects_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.TooManyRedirects("Too many redirects")

        result_str = get_weather_for_location(40, 40)
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertEqual(result_json["error"], "Too many redirects encountered when contacting weather service.")

    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_request_exception_general(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException("Some other request error")

        result_str = get_weather_for_location(50, 50)
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertTrue("An error occurred during request to weather service" in result_json["error"])
        
    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_json_decode_error(self, mock_requests_get):
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        result_str = get_weather_for_location(60,60)
        result_json = json.loads(result_str)
        self.assertIn("error", result_json)
        self.assertTrue("Failed to decode weather service response" in result_json["error"])

    @patch('FrankyX.weather_manager.tools.weather_data.requests.get')
    def test_get_weather_for_invalid_lat_lon_api_error_response(self, mock_requests_get):
        # Simulate the API returning a JSON with an error message for invalid lat/lon
        # but not necessarily a 4xx/5xx HTTP status that raise_for_status would catch.
        mock_response = Mock()
        # Open-Meteo specific error for out-of-range lat/lon
        mock_response.json.return_value = { 
            "error": True, 
            "reason": "Latitude must be in range [-90; 90]"
        }
        mock_response.raise_for_status = Mock() # Assume it doesn't raise for this type of API error
        mock_requests_get.return_value = mock_response

        result_str = get_weather_for_location(200, -300) # Invalid lat/lon
        self.assertIsInstance(result_str, str)
        result_json = json.loads(result_str)
        
        # The current tool implementation directly returns the API's JSON.
        # So we expect the API's error structure.
        self.assertIn("error", result_json)
        self.assertTrue(result_json["error"]) # API specific
        self.assertIn("reason", result_json) # API specific
        self.assertEqual(result_json["reason"], "Latitude must be in range [-90; 90]")


if __name__ == '__main__':
    # This allows running the tests directly
    # To make this work from the root of the project (e.g. /app), you might need to adjust python path
    # or run as a module: python -m FrankyX.weather_manager.tests.test_weather_data
    unittest.main()

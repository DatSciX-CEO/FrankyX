# FrankyX - AI Weather Manager

## Project Overview

FrankyX is an AI-powered weather information agent designed to provide users with accurate and timely weather forecasts, current conditions, meteorological insights, and critical weather safety guidance. It utilizes specialized tools to fetch and process weather data from external services. FrankyX aims to be a knowledgeable and reassuring assistant, helping users make informed decisions based on weather.

## Features

*   **Location Geocoding:** Converts user-provided location names (cities, zip codes, addresses) into precise geographic coordinates (latitude and longitude).
*   **Weather Data Retrieval:** Fetches current weather conditions, hourly forecasts, and daily forecasts for given coordinates.
*   **Intelligent Response Generation:** Interprets weather data to provide user-friendly information and answer weather-related questions.
*   **Error Handling:** Provides clear feedback to the user if location geocoding fails or weather data cannot be retrieved.

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd FrankyX # Or your project's root directory containing FrankyX
    ```

2.  **Create a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    # For Python 3
    python3 -m venv venv
    ```
    Or, if `python` is aliased to Python 3:
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    Ensure your virtual environment is activated. The project dependencies are listed in `FrankyX/requirements.txt`.
    ```bash
    pip install -r FrankyX/requirements.txt
    ```

5.  **Environment Variables & API Keys:**
    *   **Nominatim (Geocoding):** The `geopy` library uses Nominatim for geocoding. It's a free service and generally does not require an API key for basic usage. However, it's crucial to set a unique `user_agent` string in the code (as is done in `weather_data.py`) to comply with their usage policy and avoid potential blocks for high traffic.
    *   **Open-Meteo (Weather Data):** The Open-Meteo API is also free and does not require an API key for access.
    *   **Future API Keys:** If other services requiring API keys are integrated in the future, they would typically be managed using a `.env` file. An example workflow would be:
        1.  Copy `.env.example` to `.env`.
        2.  Fill in the required API keys in the `.env` file.
        3.  Ensure `.env` is listed in `.gitignore` to prevent committing sensitive keys.
        (Currently, `FrankyX/.env` exists and is git-ignored, ready for such use cases).

## Usage

FrankyX is designed as a component within the Google Agent Development Kit (ADK). Its primary interaction is through the `LlmAgent` framework.

**Programmatic Tool Usage Example:**

The core tool functions can also be used directly if needed, for example:

```python
import json
from FrankyX.weather_manager.tools import weather_data
from FrankyX.weather_manager.agent import root_agent # To interact with the agent

# Example 1: Direct tool usage
print("--- Direct Tool Usage Example ---")
location_name = "Eiffel Tower, Paris"
try:
    coords_json_str = weather_data.get_coordinates_for_location_string(location_name)
    print(f"Coordinates for {location_name}: {coords_json_str}")
    coords = json.loads(coords_json_str)

    if "error" not in coords:
        weather_json_str = weather_data.get_weather_for_location(coords["latitude"], coords["longitude"])
        print(f"Weather for {location_name}: {weather_json_str}")
        # weather_info = json.loads(weather_json_str)
        # Further process weather_info as needed
    else:
        print(f"Error getting coordinates: {coords.get('error')}")

except Exception as e:
    print(f"An error occurred: {e}")

# Example 2: Interacting with the ADK Agent (Conceptual)
# The actual interaction with an ADK agent depends on how it's run (e.g., within a specific ADK environment or service).
# If the agent is running and accessible, you would typically send it prompts/queries.
# For example, if `root_agent.chat()` or a similar method is available:
#
# print("\n--- Agent Interaction Example (Conceptual) ---")
# response = root_agent.chat("What's the weather like in London tomorrow?")
# print(f"FrankyX says: {response}")
#
# response_with_error = root_agent.chat("What's the weather like in NonExistentPlace123?")
# print(f"FrankyX says (for error): {response_with_error}")

# For actual execution, you'd typically run a main script that hosts and serves the ADK agent,
# or use ADK's provided tools for agent interaction.
```

(Note: The conceptual agent interaction part assumes an environment where the ADK agent is loaded and can be directly interacted with. Refer to Google ADK documentation for specific ways to run and interact with `LlmAgent` instances.)


## Testing

Unit tests are provided to ensure the functionality of the weather tools. To run the tests:

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Navigate to the root directory of the repository (the one containing the `FrankyX` directory).
3.  Run the tests using the `unittest` module:

    ```bash
    python -m unittest discover FrankyX
    ```
    Or, to run a specific test file:
    ```bash
    python -m unittest FrankyX.weather_manager.tests.test_weather_data
    ```

This will discover and run all tests within the `FrankyX` directory structure.

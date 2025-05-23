####################################################################################################
####################  FrankyX | Weather Manager - Root Agent    ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################

"""
Weather Manager Agent.  Root agent for the Weather Manager application.
This agent is responsible for managing the overall weather-related tasks and coordinating
with other agents or components as needed. 
It serves as the main entry point for the application and handles user interactions.
It is designed to be flexible and extensible, allowing for easy integration with other
components or services.
"""

from google.adk.agents import LlmAgent
from .config import WEATHER_MANAGER_MODEL # Correct: import model config
from . import prompt
from .tools import weather_data # IMPORT YOUR NEW TOOLS MODULE

# Prepare the list of tools for the agent
# The agent framework will use the function objects and their docstrings
available_tools = [
    weather_data.get_coordinates_for_location_string,
    weather_data.get_weather_for_location
]

root_agent = LlmAgent(
    name="weather_manager", # Renamed for clarity if multiple agents
    description="Root agent for the FrankyX Weather application. Manages overall weather-related tasks, including fetching and interpreting weather data using available tools.",
    model=WEATHER_MANAGER_MODEL,
    instruction=prompt.FRANKY_X_ROOT_PROMPT,
    tools=available_tools,
)
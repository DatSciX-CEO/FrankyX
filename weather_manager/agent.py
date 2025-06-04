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
from .config import WEATHER_MANAGER_GEMINI_FLASH
from .prompts import agent_prompt
from .tools import weather_data

# NEW: Simple session cache
SESSIONS = {}

def get_session(session_id: str) -> dict:
    """Creates or retrieves a session from the cache."""
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "confirmed_location": None,
            "last_weather_data": None
        }
    return SESSIONS[session_id]

# Prepare the list of tools for the agent
available_tools = [
    weather_data.get_coordinates_for_location_string,
    weather_data.get_weather_for_location
]

root_agent = LlmAgent(
    name="weather_manager",
    description="Root agent for the FrankyX Weather application. Manages overall weather-related tasks...",
    model=WEATHER_MANAGER_GEMINI_FLASH,
    instruction=agent_prompt.FRANKY_X_ROOT_PROMPT,
    tools=available_tools,
)
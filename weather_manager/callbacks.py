####################################################################################################
####################  FrankyX | Weather Manager - Root Agent - Callback  ###########################
####################  Developed by: DatSciX                              ###########################
####################################################################################################

"""
Weather Manager Agent Callbacks
These callbacks are triggered by the ADK framework after tool execution and model output generation.
They are used to implement guardrails and safety checks for the weather manager application.
"""

import json
import logging
from google.adk.agents import LlmAgentOutput
from google.adk.sessions import Session

# --- Configuration ---
# Set up a logger for our callbacks to provide detailed operational insight
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define constants for rule thresholds to make the code clean and easy to modify.
# Values are taken directly from the FRANKY_X_ROOT_PROMPT.
TORNADO_GUST_KMH = 80
BLIZZARD_WIND_KMH = 56
BLIZZARD_TEMP_C = 0
FLOOD_PRECIP_MM = 25
EXTREME_HEAT_C = 35
EXTREME_COLD_C = 0
HIGH_WIND_KMH = 40
HIGH_UV_INDEX = 6
MODERATE_PRECIP_PROB = 60

# --- Helper Functions for Guardrails ---
# These helpers check for specific conditions based on the raw weather data.

def _get_daily_data(data: dict, key: str, default: any = None):
    """Safely retrieves a value from the 'daily' data dictionary."""
    return data.get("daily", {}).get(key, default)

def _check_tornadic_conditions(data: dict) -> bool:
    """Checks for TIER 3 Tornadic Conditions."""
    has_severe_thunderstorm = any(code in [95, 96, 99] for code in _get_daily_data(data, "weather_code", []))
    has_high_gusts = max(_get_daily_data(data, "wind_gusts_10m_max", [0])) > TORNADO_GUST_KMH
    return has_severe_thunderstorm and has_high_gusts

def _check_blizzard_conditions(data: dict) -> bool:
    """Checks for TIER 3 Blizzard Conditions."""
    is_heavy_snow = 75 in _get_daily_data(data, "weather_code", [])
    has_high_winds = max(_get_daily_data(data, "wind_speed_10m_max", [0])) > BLIZZARD_WIND_KMH
    is_freezing = max(_get_daily_data(data, "temperature_2m_max", [1])) < BLIZZARD_TEMP_C
    return is_heavy_snow and has_high_winds and is_freezing

def _check_flood_watch(data: dict) -> bool:
    """Checks for TIER 2 Flood Watch."""
    return max(_get_daily_data(data, "precipitation_sum", [0])) > FLOOD_PRECIP_MM

def _check_ice_storm(data: dict) -> bool:
    """Checks for TIER 2 Ice/Freezing Rain."""
    return any(code in [66, 67] for code in _get_daily_data(data, "weather_code", []))

def _check_extreme_temps(data: dict) -> bool:
    """Checks for TIER 2 Extreme Temperatures."""
    is_extreme_heat = max(_get_daily_data(data, "apparent_temperature_max", [0])) > EXTREME_HEAT_C
    is_extreme_cold = min(_get_daily_data(data, "apparent_temperature_min", [100])) < EXTREME_COLD_C
    return is_extreme_heat or is_extreme_cold

def _check_dense_fog(data: dict) -> bool:
    """Checks for TIER 2 Dense Fog."""
    return any(code in [45, 48] for code in _get_daily_data(data, "weather_code", []))

def _check_high_winds(data: dict) -> bool:
    """Checks for TIER 1 High Winds."""
    return max(_get_daily_data(data, "wind_speed_10m_max", [0])) > HIGH_WIND_KMH

def _check_uv_index(data: dict) -> bool:
    """Checks for TIER 1 High UV Index."""
    return max(_get_daily_data(data, "uv_index_max", [0])) >= HIGH_UV_INDEX

def _check_moderate_precipitation(data: dict) -> bool:
    """Checks for TIER 1 Moderate Precipitation."""
    return max(_get_daily_data(data, "precipitation_probability_max", [0])) > MODERATE_PRECIP_PROB


# --- Main Callback Functions ---

def after_tool_callback(tool_name: str, result: str, session: Session):
    """
    This function is called by the ADK framework after any tool executes.
    It logs the raw tool output and saves critical data to the session state.
    """
    logger.info(f"CALLBACK [Tool Executed]: '{tool_name}'")
    state = session.get_state()
    
    try:
        data = json.loads(result)
        if tool_name == "get_weather_for_location":
            state["raw_weather_data"] = data
            logger.info("CALLBACK [State Update]: Stored raw weather data in session.")
        elif tool_name == "get_coordinates_for_location_string" and "full_address" in data:
            state["confirmed_location"] = data["full_address"]
            logger.info(f"CALLBACK [State Update]: Stored confirmed location '{data['full_address']}'.")
    except (json.JSONDecodeError, TypeError):
        logger.error(f"CALLBACK [Error]: Failed to decode JSON from tool '{tool_name}'.")
    
    session.set_state(state)


def after_model_callback(output: LlmAgentOutput, session: Session) -> LlmAgentOutput:
    """
    This function is our main programmatic GUARDRAIL engine.
    It validates the agent's final response against every rule in the prompt.
    """
    logger.info("GUARDRAIL [Validation Start]: Checking final model output for safety compliance.")
    state = session.get_state()
    raw_weather_data = state.get("raw_weather_data")

    if not isinstance(raw_weather_data, dict):
        logger.warning("GUARDRAIL [Skipped]: No valid weather data in session to validate against.")
        return output

    # --- TIER 3: SEVERE WEATHER ALERTS (MUST BE PRESENT) ---
    if _check_tornadic_conditions(raw_weather_data) and "SEVERE WEATHER ALERT: TORNADO POTENTIAL" not in output.text:
        logger.critical("GUARDRAIL VIOLATION: LLM failed to include mandatory Tornado Potential alert!")
        output.text = "I have detected a potentially severe weather event, but I am unable to generate the specific safety alert. Please consult your local weather authority immediately."
        return output # Stop further processing

    if _check_blizzard_conditions(raw_weather_data) and "SEVERE WEATHER ALERT: BLIZZARD CONDITIONS" not in output.text:
        logger.critical("GUARDRAIL VIOLATION: LLM failed to include mandatory Blizzard Conditions alert!")
        output.text = "I have detected a potentially severe weather event, but I am unable to generate the specific safety alert. Please consult your local weather authority immediately."
        return output # Stop further processing

    # --- TIER 2 & 1: ADVISORIES (LOG IF MISSING) ---
    # For these, we log a warning but don't override the output, as it's less critical.
    # This helps monitor the LLM's reliability.
    if _check_flood_watch(raw_weather_data) and "Flood Watch" not in output.text:
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including a Flood Watch advisory.")
    
    if _check_ice_storm(raw_weather_data) and "Ice Storm Advisory" not in output.text:
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including an Ice Storm Advisory.")

    if _check_extreme_temps(raw_weather_data) and not ("Heat Advisory" in output.text or "Cold Advisory" in output.text):
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including an Extreme Temperature Advisory.")
        
    if _check_dense_fog(raw_weather_data) and "Dense Fog Advisory" not in output.text:
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including a Dense Fog Advisory.")
        
    if _check_high_winds(raw_weather_data) and "High Winds" not in output.text:
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including a High Winds advisory.")
        
    if _check_uv_index(raw_weather_data) and "High UV Index" not in output.text:
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including a High UV Index advisory.")
        
    if _check_moderate_precipitation(raw_weather_data) and "prepare for wet or slick conditions" not in output.text:
        logger.warning("GUARDRAIL NOTICE: LLM may have missed including a Moderate Precipitation advisory.")

    logger.info("GUARDRAIL [Validation Complete]: Output conforms to critical safety standards.")
    return output
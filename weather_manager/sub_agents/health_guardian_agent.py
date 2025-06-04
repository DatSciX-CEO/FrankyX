####################################################################################################
####################  FrankyX | Health Guardian SubAgent        ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################

"""
Health Guardian SubAgent
This sub-agent is designed to assess health risks related to weather conditions and provide actionable advice to mitigate those risks.
"""

from google.adk.agents import LlmAgent
from ..config import HEALTH_GUARDIAN_GEMINI_FLASH
from ..tools import health_impact_tools
from ..prompts import health_prompt

health_guardian_agent = LlmAgent(
    name="health_guardian",
    description="Specializes in weather-related health impacts and medical safety",
    model=HEALTH_GUARDIAN_GEMINI_FLASH,
    instruction=health_prompt.HEALTH_GUARDIAN_PROMPT,
    tools=[
        health_impact_tools.calculate_heat_index_risk,
        health_impact_tools.calculate_cold_exposure_risk,
        health_impact_tools.assess_air_quality_impact,
        health_impact_tools.calculate_uv_exposure_risk,
        health_impact_tools.get_pressure_change_impacts,
        health_impact_tools.get_allergen_forecast
    ]
)
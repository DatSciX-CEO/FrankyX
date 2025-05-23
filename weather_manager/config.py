####################################################################################################
####################  FrankyX | Application Configuration       ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################

"""
Configuration settings for the FrankyX application.
This module loads settings from environment variables (typically defined in a .env file).
It provides a central place for all configuration values used by the application.
"""

from google.adk.models.lite_llm import LiteLlm

# LLM Model Configuration:
WEATHER_MANAGER_MODEL = LiteLlm(model="ollama_chat/gemma3:4b", temperature=0.75)
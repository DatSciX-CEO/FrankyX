####################################################################################################
####################  FrankyX | Health Impact - Tools           ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################

"""
Health Impact Tools
These tools assess health risks from heat exposure and air quality.
They provide detailed recommendations based on environmental conditions.
"""

import json
from typing import Dict, List
from datetime import datetime

def calculate_heat_index_risk(
    temperature_c: float,
    humidity_percent: float,
    duration_hours: float = 1.0
) -> str:
    """
    Calculates health risks from heat exposure.
    
    Returns:
        JSON string with heat risk assessment and recommendations
    """
    # Heat index calculation (simplified version)
    temp_f = (temperature_c * 9/5) + 32
    
    if temp_f < 80:
        heat_index = temp_f
    else:
        # Rothfusz regression
        heat_index = (-42.379 + 2.04901523 * temp_f + 10.14333127 * humidity_percent
                     - 0.22475541 * temp_f * humidity_percent - 0.00683783 * temp_f**2
                     - 0.05481717 * humidity_percent**2 + 0.00122874 * temp_f**2 * humidity_percent
                     + 0.00085282 * temp_f * humidity_percent**2 - 0.00000199 * temp_f**2 * humidity_percent**2)
    
    # Risk categorization
    if heat_index >= 130:
        risk_level = "EXTREME"
        health_effects = "Heat stroke highly likely. LIFE-THREATENING CONDITIONS."
    elif heat_index >= 105:
        risk_level = "DANGEROUS"
        health_effects = "Heat stroke probable with prolonged exposure."
    elif heat_index >= 90:
        risk_level = "HIGH"
        health_effects = "Heat exhaustion possible. Muscle cramps likely."
    elif heat_index >= 80:
        risk_level = "MODERATE"
        health_effects = "Fatigue possible with prolonged exposure."
    else:
        risk_level = "LOW"
        health_effects = "Minimal heat stress risk for most people."
    
    risk_assessment = {
        "heat_index_f": round(heat_index, 1),
        "heat_index_c": round((heat_index - 32) * 5/9, 1),
        "risk_level": risk_level,
        "health_effects": health_effects,
        "vulnerable_groups": {
            "elderly": {
                "risk_multiplier": 1.5,
                "special_concerns": ["Reduced sweating ability", "Medication interactions"]
            },
            "children": {
                "risk_multiplier": 1.3,
                "special_concerns": ["Higher metabolic rate", "Less efficient cooling"]
            },
            "chronic_conditions": {
                "heart_disease": "Increased cardiac strain",
                "diabetes": "Impaired temperature regulation",
                "obesity": "Reduced heat dissipation"
            }
        },
        "recommendations": {
            "hydration": {
                "water_oz_per_hour": max(8, int(heat_index / 10)),
                "electrolyte_replacement": heat_index > 90,
                "avoid": ["Alcohol", "Caffeine", "Sugary drinks"]
            },
            "activity": {
                "outdoor_work": "Limit to early morning or evening" if heat_index > 90 else "Take frequent breaks",
                "exercise": "Move indoors" if heat_index > 95 else "Reduce intensity",
                "rest_breaks": f"Every {30 if heat_index > 100 else 60} minutes"
            },
            "cooling": {
                "methods": ["Air conditioning", "Cool showers", "Wet towels"],
                "clothing": "Light-colored, loose-fitting, breathable fabrics"
            }
        },
        "warning_signs": {
            "heat_exhaustion": [
                "Heavy sweating", 
                "Weakness", 
                "Nausea", 
                "Headache", 
                "Muscle cramps"
            ],
            "heat_stroke": [
                "No sweating",
                "Hot, dry skin",
                "Confusion",
                "Loss of consciousness",
                "Body temp > 103°F"
            ],
            "action": "Call 911 immediately for heat stroke symptoms"
        }
    }
    
    return json.dumps(risk_assessment)

def assess_air_quality_impact(
    pm25: float,
    pm10: float,
    ozone: float,
    existing_conditions: List[str] = None
) -> str:
    """
    Assesses health impacts from air quality.
    
    Returns:
        JSON string with air quality health assessment
    """
    # AQI calculation (simplified)
    aqi = max(
        calculate_aqi_component(pm25, [(0, 12), (12.1, 35.4), (35.5, 55.4), (55.5, 150.4)]),
        calculate_aqi_component(pm10, [(0, 54), (55, 154), (155, 254), (255, 354)]),
        calculate_aqi_component(ozone, [(0, 54), (55, 70), (71, 85), (86, 105)])
    )
    
    # Categorize health impacts
    if aqi <= 50:
        category = "Good"
        health_message = "Air quality is satisfactory with little or no risk."
    elif aqi <= 100:
        category = "Moderate"
        health_message = "Unusually sensitive individuals may experience minor symptoms."
    elif aqi <= 150:
        category = "Unhealthy for Sensitive Groups"
        health_message = "Sensitive groups may experience health effects."
    elif aqi <= 200:
        category = "Unhealthy"
        health_message = "Everyone may begin to experience health effects."
    else:
        category = "Very Unhealthy"
        health_message = "Health warnings of emergency conditions."
    
    assessment = {
        "aqi": aqi,
        "category": category,
        "health_message": health_message,
        "pollutant_levels": {
            "pm25": {"value": pm25, "unit": "μg/m³"},
            "pm10": {"value": pm10, "unit": "μg/m³"},
            "ozone": {"value": ozone, "unit": "ppb"}
        },
        "sensitive_groups": {
            "respiratory": {
                "conditions": ["Asthma", "COPD", "Emphysema"],
                "risk_level": "HIGH" if aqi > 100 else "MODERATE",
                "recommendations": [
                    "Keep rescue medications nearby",
                    "Monitor symptoms closely",
                    "Limit outdoor exposure" if aqi > 100 else "Reduce prolonged exertion"
                ]
            },
            "cardiovascular": {
                "conditions": ["Heart disease", "Arrhythmias"],
                "risk_level": "MODERATE" if aqi > 100 else "LOW",
                "recommendations": ["Avoid strenuous activities", "Monitor heart rate"]
            },
            "children": {
                "risk_level": "MODERATE" if aqi > 50 else "LOW",
                "recommendations": ["Limit outdoor playtime", "Move activities indoors"]
            }
        },
        "protective_measures": {
            "outdoors": {
                "mask_recommended": aqi > 150,
                "mask_type": "N95 or P100" if aqi > 150 else "Not necessary",
                "activity_level": "Minimize" if aqi > 150 else "Reduce" if aqi > 100 else "Normal"
            },
            "indoors": {
                "windows": "Keep closed" if aqi > 100 else "OK to open",
                "air_purifier": "Recommended" if aqi > 100 else "Optional",
                "hvac_filter": "MERV 13+" if aqi > 150 else "Standard"
            }
        }
    }
    
    return json.dumps(assessment)

def calculate_aqi_component(concentration: float, breakpoints: List[tuple]) -> int:
    """Helper function for AQI calculation."""
    for i, (low, high) in enumerate(breakpoints):
        if low <= concentration <= high:
            return int(((i * 50) + 50) * (concentration - low) / (high - low))
    return 500  # Beyond AQI scale
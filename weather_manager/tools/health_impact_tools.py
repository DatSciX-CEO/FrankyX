####################################################################################################
####################  FrankyX | Health Impact - Tools           ####################################
####################  Developed by: DatSciX                     ####################################
####################################################################################################

"""
Health Impact Tools for Weather Manager
This module provides functions to assess health risks related to weather conditions,
including heat and cold exposure, air quality, UV radiation, and barometric pressure changes.
It includes detailed risk assessments, recommendations for vulnerable groups, and protective measures.
"""

import json
from typing import Dict, List, Optional

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


def calculate_cold_exposure_risk(
    temperature_c: float,
    wind_speed_kph: float,
    duration_hours: float = 1.0,
    precipitation: bool = False
) -> str:
    """
    Calculates health risks from cold exposure including wind chill.
    
    Returns:
        JSON string with cold risk assessment and recommendations
    """
    temp_f = (temperature_c * 9/5) + 32
    wind_mph = wind_speed_kph * 0.621371
    
    # Wind chill calculation (NWS formula)
    if temp_f <= 50 and wind_mph >= 3:
        wind_chill_f = (35.74 + 0.6215 * temp_f - 35.75 * (wind_mph ** 0.16) 
                        + 0.4275 * temp_f * (wind_mph ** 0.16))
    else:
        wind_chill_f = temp_f
    
    wind_chill_c = (wind_chill_f - 32) * 5/9
    
    # Risk categorization based on exposure time
    if wind_chill_f <= -35:
        risk_level = "EXTREME"
        frostbite_time = "5 minutes"
        health_effects = "Exposed skin freezes in minutes. Life-threatening."
    elif wind_chill_f <= -15:
        risk_level = "DANGEROUS"
        frostbite_time = "10 minutes"
        health_effects = "Frostbite likely on exposed skin."
    elif wind_chill_f <= 0:
        risk_level = "HIGH"
        frostbite_time = "30 minutes"
        health_effects = "Frostbite possible on exposed skin."
    elif wind_chill_f <= 32:
        risk_level = "MODERATE"
        frostbite_time = "Extended exposure"
        health_effects = "Hypothermia risk with prolonged exposure."
    else:
        risk_level = "LOW"
        frostbite_time = "Not applicable"
        health_effects = "Minimal cold stress for properly dressed individuals."
    
    # Adjust for precipitation
    if precipitation and temp_f <= 35:
        risk_level = "HIGH" if risk_level == "MODERATE" else risk_level
        additional_risk = "Wet conditions significantly increase heat loss"
    else:
        additional_risk = None
    
    risk_assessment = {
        "temperature_f": round(temp_f, 1),
        "temperature_c": round(temperature_c, 1),
        "wind_chill_f": round(wind_chill_f, 1),
        "wind_chill_c": round(wind_chill_c, 1),
        "risk_level": risk_level,
        "frostbite_time": frostbite_time,
        "health_effects": health_effects,
        "additional_risk": additional_risk,
        "vulnerable_groups": {
            "elderly": {
                "risk_factors": ["Reduced circulation", "Medication effects", "Mobility issues"],
                "special_precautions": "Limit outdoor exposure, check frequently"
            },
            "children": {
                "risk_factors": ["Higher surface area to volume ratio", "Less awareness of cold"],
                "special_precautions": "Dress in layers, limit outdoor play time"
            },
            "homeless": {
                "risk_factors": ["Extended exposure", "Inadequate shelter"],
                "resources": "Warming center locations, emergency shelters"
            },
            "outdoor_workers": {
                "risk_factors": ["Prolonged exposure", "Physical exertion"],
                "osha_guidelines": "Mandatory warm-up breaks every hour"
            }
        },
        "protective_measures": {
            "clothing": {
                "layers": ["Moisture-wicking base", "Insulating middle", "Windproof outer"],
                "extremities": "Insulated gloves, warm socks, face covering",
                "materials": "Avoid cotton, use wool or synthetic"
            },
            "shelter": {
                "heating": "Maintain indoor temp above 68°F",
                "emergency": "Have backup heat source",
                "carbon_monoxide": "Never use outdoor heaters indoors"
            },
            "activity": {
                "work_rest_cycle": f"{60 - int(wind_chill_f)} min work / {int(60 - wind_chill_f) / 4} min warm-up",
                "exercise": "Move indoors" if wind_chill_f < 20 else "Reduce duration",
                "travel": "Emergency kit in vehicle" if wind_chill_f < 32 else "Normal precautions"
            }
        },
        "warning_signs": {
            "hypothermia": [
                "Shivering",
                "Confusion",
                "Slurred speech",
                "Drowsiness",
                "Weak pulse"
            ],
            "frostbite": [
                "Numbness",
                "Skin color changes",
                "Hard or waxy skin",
                "Blistering (after rewarming)"
            ],
            "action": "Seek immediate medical attention for severe symptoms"
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


def calculate_uv_exposure_risk(
    uv_index: float,
    skin_type: Optional[int] = None,
    duration_minutes: int = 30
) -> str:
    """
    Calculates UV exposure risks and sun protection recommendations.
    
    Args:
        uv_index: Current UV index value
        skin_type: Fitzpatrick skin type (1-6), None for general advice
        duration_minutes: Expected exposure duration
        
    Returns:
        JSON string with UV risk assessment and protection measures
    """
    # UV risk categories
    if uv_index >= 11:
        risk_category = "EXTREME"
        burn_time_fair = 10
    elif uv_index >= 8:
        risk_category = "VERY HIGH"
        burn_time_fair = 15
    elif uv_index >= 6:
        risk_category = "HIGH"
        burn_time_fair = 20
    elif uv_index >= 3:
        risk_category = "MODERATE"
        burn_time_fair = 30
    else:
        risk_category = "LOW"
        burn_time_fair = 60
    
    # Skin type burn times (multipliers for fair skin baseline)
    skin_type_factors = {
        1: 0.7,   # Very fair, always burns
        2: 1.0,   # Fair, usually burns
        3: 1.5,   # Light, sometimes burns
        4: 2.0,   # Medium, rarely burns
        5: 3.0,   # Dark, very rarely burns
        6: 4.0    # Very dark, never burns
    }
    
    if skin_type and skin_type in skin_type_factors:
        burn_time = int(burn_time_fair * skin_type_factors[skin_type])
        skin_specific = True
    else:
        burn_time = burn_time_fair
        skin_specific = False
    
    # Calculate accumulated exposure risk
    exposure_ratio = duration_minutes / burn_time
    if exposure_ratio >= 3:
        exposure_risk = "SEVERE - Multiple sunburns likely"
    elif exposure_ratio >= 1.5:
        exposure_risk = "HIGH - Sunburn likely"
    elif exposure_ratio >= 0.5:
        exposure_risk = "MODERATE - Sunburn possible"
    else:
        exposure_risk = "LOW - Minimal burn risk"
    
    risk_assessment = {
        "uv_index": uv_index,
        "risk_category": risk_category,
        "burn_time_minutes": burn_time,
        "skin_type_considered": skin_specific,
        "planned_exposure": {
            "duration_minutes": duration_minutes,
            "exposure_risk": exposure_risk,
            "spf_recommended": max(15, int(uv_index * 3))
        },
        "health_risks": {
            "immediate": ["Sunburn", "Eye damage", "Heat exhaustion"],
            "long_term": ["Skin cancer", "Premature aging", "Cataracts"],
            "vulnerable_groups": {
                "children": "80% of lifetime sun exposure occurs before age 18",
                "medications": "Some medications increase photosensitivity",
                "conditions": "Lupus, albinism require extra protection"
            }
        },
        "protection_measures": {
            "timing": {
                "avoid_hours": "10 AM - 4 PM" if uv_index >= 6 else "Peak midday",
                "shadow_rule": "Seek shade when shadow shorter than height"
            },
            "sunscreen": {
                "spf": max(30, int(uv_index * 3)),
                "application": "2mg/cm² - about 1oz for full body",
                "reapply": "Every 2 hours or after swimming/sweating",
                "type": "Broad spectrum, water-resistant"
            },
            "clothing": {
                "coverage": "Long sleeves, pants" if uv_index >= 8 else "Light coverage",
                "upf_rating": "UPF 50+" if uv_index >= 6 else "UPF 30+",
                "hat": "Wide-brimmed (4 inches)" if uv_index >= 6 else "Baseball cap",
                "sunglasses": "UV400 protection essential"
            },
            "additional": {
                "shade": "Use umbrellas, trees, shelters",
                "reflection": "Extra caution near water, sand, snow",
                "altitude": "UV increases 10% per 1000m elevation"
            }
        },
        "vitamin_d_note": "15-20 minutes exposure before 10 AM provides adequate vitamin D"
    }
    
    return json.dumps(risk_assessment)


def get_pressure_change_impacts(
    current_pressure_mb: float,
    pressure_trend: str,
    change_rate_mb_per_hour: float
) -> str:
    """
    Analyzes barometric pressure changes for health impacts.
    
    Args:
        current_pressure_mb: Current pressure in millibars
        pressure_trend: "rising", "falling", or "steady"
        change_rate_mb_per_hour: Rate of pressure change
        
    Returns:
        JSON string with pressure-related health impacts
    """
    # Categorize pressure change severity
    if abs(change_rate_mb_per_hour) >= 3:
        change_severity = "RAPID"
        impact_level = "HIGH"
    elif abs(change_rate_mb_per_hour) >= 1.5:
        change_severity = "MODERATE"
        impact_level = "MODERATE"
    else:
        change_severity = "SLOW"
        impact_level = "LOW"
    
    # Determine weather implication
    if pressure_trend == "falling" and change_rate_mb_per_hour <= -3:
        weather_change = "Storm approaching rapidly"
    elif pressure_trend == "falling":
        weather_change = "Deteriorating weather expected"
    elif pressure_trend == "rising" and change_rate_mb_per_hour >= 3:
        weather_change = "Rapid weather improvement"
    elif pressure_trend == "rising":
        weather_change = "Improving weather conditions"
    else:
        weather_change = "Stable weather pattern"
    
    health_impacts = {
        "pressure_data": {
            "current_mb": current_pressure_mb,
            "current_inhg": round(current_pressure_mb * 0.02953, 2),
            "trend": pressure_trend,
            "change_rate_mb_hr": change_rate_mb_per_hour,
            "change_severity": change_severity
        },
        "weather_implication": weather_change,
        "impact_level": impact_level,
        "affected_conditions": {
            "migraines": {
                "risk_level": "HIGH" if abs(change_rate_mb_per_hour) >= 2 else "MODERATE",
                "mechanism": "Pressure changes affect blood vessel dilation",
                "symptoms": ["Throbbing headache", "Light sensitivity", "Nausea"],
                "prevention": [
                    "Take preventive medication if prescribed",
                    "Stay hydrated",
                    "Maintain regular sleep schedule",
                    "Avoid triggers (alcohol, certain foods)"
                ]
            },
            "arthritis": {
                "risk_level": "MODERATE" if abs(change_rate_mb_per_hour) >= 1.5 else "LOW",
                "mechanism": "Pressure affects joint fluid and tissues",
                "symptoms": ["Joint stiffness", "Increased pain", "Reduced mobility"],
                "management": [
                    "Gentle stretching exercises",
                    "Warm compresses on joints",
                    "Anti-inflammatory medications as prescribed",
                    "Maintain comfortable temperature"
                ]
            },
            "sinuses": {
                "risk_level": "MODERATE" if pressure_trend == "falling" else "LOW",
                "symptoms": ["Sinus pressure", "Congestion", "Facial pain"],
                "relief": [
                    "Use humidifier",
                    "Saline nasal rinse",
                    "Stay hydrated",
                    "Decongestants if needed"
                ]
            },
            "mood_disorders": {
                "risk_level": "LOW to MODERATE",
                "effects": "May experience mood changes or anxiety",
                "coping": [
                    "Maintain routine",
                    "Light therapy if gloomy",
                    "Regular exercise",
                    "Mindfulness practices"
                ]
            }
        },
        "general_recommendations": {
            "preparation": "Have medications readily available" if impact_level == "HIGH" else "Monitor symptoms",
            "activity": "Consider rescheduling strenuous activities" if impact_level == "HIGH" else "Normal activities OK",
            "medical": "Contact healthcare provider if symptoms severe"
        },
        "timeline": {
            "onset": "Symptoms may begin 6-12 hours before weather change",
            "peak": "Usually coincides with maximum pressure change",
            "duration": "Typically resolves within 24-48 hours"
        }
    }
    
    return json.dumps(health_impacts)


def get_allergen_forecast(
    location: Dict[str, float],
    season: str,
    recent_precipitation: bool = False
) -> str:
    """
    Provides allergen forecasts and allergy management recommendations.
    
    Args:
        location: Dict with latitude and longitude
        season: Current season
        recent_precipitation: Whether it rained recently
        
    Returns:
        JSON string with allergen levels and recommendations
    """
    # Seasonal allergen patterns (simplified model)
    seasonal_allergens = {
        "spring": {
            "tree_pollen": "HIGH",
            "grass_pollen": "MODERATE",
            "weed_pollen": "LOW",
            "mold": "MODERATE"
        },
        "summer": {
            "tree_pollen": "LOW",
            "grass_pollen": "HIGH",
            "weed_pollen": "MODERATE",
            "mold": "MODERATE"
        },
        "fall": {
            "tree_pollen": "LOW",
            "grass_pollen": "LOW",
            "weed_pollen": "HIGH",
            "mold": "HIGH"
        },
        "winter": {
            "tree_pollen": "LOW",
            "grass_pollen": "LOW",
            "weed_pollen": "LOW",
            "mold": "LOW"
        }
    }
    
    current_levels = seasonal_allergens.get(season.lower(), seasonal_allergens["spring"])
    
    # Adjust for recent rain
    if recent_precipitation:
        pollen_modifier = "Temporarily reduced (rain washout)"
        mold_modifier = "May increase in 24-48 hours"
    else:
        pollen_modifier = "Normal for season"
        mold_modifier = "Normal for season"
    
    # Calculate overall allergy index
    high_count = sum(1 for level in current_levels.values() if level == "HIGH")
    if high_count >= 2:
        overall_index = "HIGH"
        severity = "Significant allergy symptoms expected"
    elif high_count == 1 or sum(1 for level in current_levels.values() if level == "MODERATE") >= 2:
        overall_index = "MODERATE"
        severity = "Moderate allergy symptoms possible"
    else:
        overall_index = "LOW"
        severity = "Minimal allergy symptoms expected"
    
    allergen_forecast = {
        "location": location,
        "season": season,
        "overall_index": overall_index,
        "severity": severity,
        "allergen_levels": {
            "tree_pollen": {
                "level": current_levels["tree_pollen"],
                "status": pollen_modifier,
                "common_trees": ["Oak", "Birch", "Cedar", "Pine"] if season == "spring" else []
            },
            "grass_pollen": {
                "level": current_levels["grass_pollen"],
                "status": pollen_modifier,
                "peak_times": "5-10 AM on dry, windy days"
            },
            "weed_pollen": {
                "level": current_levels["weed_pollen"],
                "status": pollen_modifier,
                "primary_culprit": "Ragweed" if season == "fall" else "Various"
            },
            "mold": {
                "level": current_levels["mold"],
                "status": mold_modifier,
                "conditions": "Thrives in damp, humid conditions"
            }
        },
        "symptom_management": {
            "medications": {
                "preventive": [
                    "Start antihistamines before symptoms",
                    "Nasal corticosteroids for congestion",
                    "Eye drops for itchy eyes"
                ],
                "timing": "Take medications 30 min before going outside"
            },
            "environmental": {
                "outdoors": [
                    "Wear wraparound sunglasses",
                    "Avoid peak pollen hours (5-10 AM)",
                    "Shower and change clothes after outdoor activities"
                ],
                "indoors": [
                    "Keep windows closed",
                    "Use HEPA air filters",
                    "Run AC instead of fans",
                    "Vacuum with HEPA filter twice weekly"
                ]
            },
            "natural_remedies": [
                "Saline nasal rinse",
                "Local honey (may help with pollen)",
                "Quercetin supplements",
                "Butterbur extract"
            ]
        },
        "high_risk_activities": {
            "avoid": [
                "Mowing grass",
                "Raking leaves",
                "Hanging laundry outside",
                "Outdoor exercise during peak hours"
            ],
            "alternatives": [
                "Delegate yard work or wear N95 mask",
                "Exercise indoors on high pollen days",
                "Use dryer for laundry",
                "Plan outdoor activities for late afternoon"
            ]
        },
        "tracking_advice": "Monitor daily pollen counts and plan accordingly"
    }
    
    return json.dumps(allergen_forecast)


def calculate_aqi_component(concentration: float, breakpoints: List[tuple]) -> int:
    """Helper function for AQI calculation."""
    for i, (low, high) in enumerate(breakpoints):
        if low <= concentration <= high:
            return int(((i * 50) + 50) * (concentration - low) / (high - low))
    return 500  # Beyond AQI scale
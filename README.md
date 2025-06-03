# 🌤️ FrankyX - Your AI Weather Guardian 🛡️

<div align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/Weather-Safety-green?style=for-the-badge" alt="Weather Safety"/>
  <img src="https://img.shields.io/badge/Built%20with-Google%20ADK-red?style=for-the-badge" alt="Google ADK"/>
  <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge" alt="Python 3.8+"/>
</div>

<div align="center">
  <h3>🌪️ Because Mother Nature Doesn't Send Calendar Invites 🌪️</h3>
  <p><i>An intelligent AI agent that not only tells you the weather but actively protects you from it!</i></p>
</div>

---

## 🎯 What is FrankyX?

**FrankyX** is your personal AI meteorologist that goes beyond simple weather forecasts. Built with Google's Agent Development Kit (ADK), FrankyX analyzes weather patterns, identifies potential dangers, and provides life-saving safety recommendations - all in a conversational, friendly manner.

Think of FrankyX as your weather-savvy friend who:
- 🔍 Always double-checks locations before giving you weather info
- ⚡ Spots dangerous conditions before they become emergencies
- 💬 Explains weather in plain English (no meteorology degree required!)
- 🚨 Takes your safety seriously with tiered alert systems

## ✨ Features That Make FrankyX Special

### 🛡️ **Three-Tier Safety System**
- **🔴 TIER 3 - SEVERE**: Tornado potential, blizzard conditions (Immediate action required!)
- **🟡 TIER 2 - ELEVATED**: Floods, ice storms, extreme temps (Stay alert!)
- **🟢 TIER 1 - GENERAL**: High winds, UV index, rain (Be prepared!)

### 🤖 **AI-Powered Intelligence**
- 🧠 Powered by Gemini & Ollama LLMs for natural conversations
- 📍 Smart location detection with confirmation (no more wrong city weather!)
- 🌡️ Automatic Fahrenheit conversion for US users
- 📊 Comprehensive weather analysis including "feels like" temperature

### 🔧 **Developer-Friendly**
- 🏗️ Modular architecture for easy extension
- 🧪 Unit test ready
- 📝 Clean, documented code
- 🔌 No API keys required (uses free services!)

## 🚀 Quick Start Guide

### 📋 Prerequisites

Before you invite FrankyX into your terminal, make sure you have:

- 🐍 Python 3.8 or higher
- 📦 pip (Python package manager)
- 💻 Git
- 🌐 Internet connection (FrankyX needs to check the weather!)

### 🛠️ Installation

#### 1️⃣ **Clone the Repository**

```bash
# Get FrankyX on your machine
git clone https://github.com/DatSciX-CEO/FrankyX.git
cd FrankyX
```

#### 2️⃣ **Set Up Your Virtual Environment** 

```bash
# Create a cozy virtual environment for FrankyX
python -m venv venv

# Activate it:
# On Windows 🪟
venv\Scripts\activate

# On macOS/Linux 🐧🍎
source venv/bin/activate
```

#### 3️⃣ **Install Dependencies**

```bash
# Let FrankyX gather its tools
pip install -r requirements.txt
```

#### 4️⃣ **Configure Environment** (Optional)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if you need custom configurations
# (Currently, FrankyX uses free APIs - no keys needed! 🎉)
```

## 🎮 How to Use FrankyX

### 🔬 Direct Tool Usage

```python
import json
from weather_manager.tools import weather_data

# Ask FrankyX about the weather
location = "Times Square, NYC"
coords = json.loads(weather_data.get_coordinates_for_location_string(location))

if "error" not in coords:
    weather = weather_data.get_weather_for_location(
        coords["latitude"], 
        coords["longitude"]
    )
    print(f"Weather data: {weather}")
```

### 🤖 Using the AI Agent

```python
from weather_manager.agent import root_agent

# Have a conversation with FrankyX
response = root_agent.chat("What's the weather like in Seattle tomorrow?")
print(f"FrankyX says: {response}")

# FrankyX handles errors gracefully
response = root_agent.chat("Weather in Atlantis?")
print(f"FrankyX says: {response}")  # Will politely explain it can't find Atlantis
```

### 🧪 Running Tests

```bash
# Make sure FrankyX is working correctly
python -m unittest discover weather_manager

# Run specific test modules
python -m unittest weather_manager.tests.test_weather_data
```

## 🌟 Example Conversations

### 💬 Basic Weather Query
```
You: "What's the weather in Chicago?"
FrankyX: "I found Chicago, Cook County, Illinois, United States. Is this correct?"
You: "Yes"
FrankyX: "Current conditions in Chicago: 45°F (feels like 41°F)..."
```

### 🚨 Safety Alert Example
```
You: "Weather in Kansas during tornado season?"
FrankyX: "⚠️ SEVERE WEATHER ALERT: TORNADO POTENTIAL ⚠️
The forecast shows severe thunderstorms with 65 mph wind gusts...
IMMEDIATE PRECAUTIONS REQUIRED:
• SEEK SHELTER NOW..."
```

## 🏗️ Project Structure

```
FrankyX/
├── 🎯 weather_manager/
│   ├── 🤖 agent.py          # The brain of FrankyX
│   ├── 💭 prompt.py         # FrankyX's personality
│   ├── ⚙️ config.py         # Configuration settings
│   ├── 🔧 tools/           
│   │   └── 🌤️ weather_data.py  # Weather fetching tools
│   ├── 🧪 tests/            # Test suite
│   └── 📁 services/         # Future expansion
├── 📋 requirements.txt      # Python dependencies
├── 🔒 .env.example         # Environment template
└── 📖 README.md            # You are here! 👋
```

## 🛡️ Safety Features Deep Dive

FrankyX takes weather safety seriously. Here's how the protection system works:

### 🌪️ **Tornado Detection**
- Monitors for severe thunderstorm codes (95, 96, 99)
- Checks wind gusts exceeding 50 mph
- Provides immediate shelter instructions

### ❄️ **Blizzard Warning**
- Detects heavy snow (code 75) + high winds + freezing temps
- Advises against travel
- Recommends emergency preparations

### 🌊 **Flood Watch**
- Monitors 24-hour precipitation exceeding 1 inch
- Warns about flash flood risks
- Emphasizes "Turn Around, Don't Drown"

## 🤝 Contributing

We love contributions! Here's how you can help make FrankyX even better:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingWeatherFeature`)
3. 💾 Commit your changes (`git commit -m 'Add hurricane tracking'`)
4. 📤 Push to the branch (`git push origin feature/AmazingWeatherFeature`)
5. 🎉 Open a Pull Request

### 💡 Contribution Ideas
- 🌍 Add support for international weather alerts
- 📱 Create a web interface
- 🔔 Implement push notifications
- 🌐 Add more language support
- 📊 Enhance data visualization

## 🐛 Found a Bug?

If FrankyX gives you sunny skies during a thunderstorm:

1. Check if you're using the latest version
2. Search existing issues
3. Create a new issue with:
   - 🐛 Bug description
   - 🔄 Steps to reproduce
   - 💻 Your environment details
   - 📸 Screenshots (if applicable)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🌤️ [Open-Meteo](https://open-meteo.com/) for free weather data
- 📍 [Nominatim](https://nominatim.org/) for geocoding services
- 🤖 [Google ADK](https://github.com/google/genai-agent-dev-kit) for the agent framework
- 🌟 All contributors who help keep users safe!

## 📞 Contact & Support

- 👨‍💻 **Developer**: DatSciX
- 🐙 **GitHub**: [@DatSciX-CEO](https://github.com/DatSciX-CEO)
- 🐛 **Issues**: [GitHub Issues](https://github.com/DatSciX-CEO/FrankyX/issues)

---

<div align="center">
  <h3>🌈 Stay Safe, Stay Informed with FrankyX! 🌈</h3>
  <p><i>Remember: When FrankyX says seek shelter, you seek shelter! 🏃‍♂️💨</i></p>
  
  ⭐ **If FrankyX helped you avoid bad weather, give us a star!** ⭐
</div>
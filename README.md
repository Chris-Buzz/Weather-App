**Weather App 🌦️*\n
This Weather App helps users plan their day by providing weather forecasts based on their location. The app uses the OpenWeatherMap API to fetch real-time weather data.

**Features**
Current weather data for a specified location
5-day weather forecast - free version of OpenWeatherMap
Intuitive design optimized for both web and mobile

**How It Works**
Backend Development
The backend is coded in Python, where it communicates with the OpenWeatherMap API to fetch weather data based on user input (e.g., city name, ZIP code, or GPS coordinates).
Current Frontend:
  Frontend is currently made with a simple tkinter design

**API Calls**
The app interacts with the following OpenWeatherMap endpoints:
Current Weather Data:
https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
7-Day Weather Forecast:
https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={API key}
API Key Setup

**To use the OpenWeatherMap API:**

Create an account on OpenWeatherMap.
Navigate to your account settings and generate an API key under the "API Keys" section.
Copy the key and add it to your project environment file (e.g., .env) as:
makefile
Copy code
OPENWEATHER_API_KEY=your_api_key

Here’s an example of fetching weather data for New York City:

import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "New York",
    "appid": API_KEY,
    "units": "metric"  # Use "imperial" for Fahrenheit
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    print("Temperature:", data["main"]["temp"], "°C")
else:
    print("Error:", response.status_code)

**Currently In Development**
  Right now the weather app is in a basic tkinter GUI framework design
  My friend who studies graphic design is working on making a custom frontend design in Figma
  Once completed Figma design will be transferred to html & css and using either py-script, flask or django the backend python will be implemented into the design

  **New Feautures**
    Providing a daily planner for users so they can plan their days based on weather
    Provide users outfit reccomendations based on the current weather to help them choose what to wear
  

import requests
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz


def get_weather(event=None):
    city = textfield.get()
    api_key = "27813a1f3eb806c48f81c63fe6e371af"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=imperial"

    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        city_name = weather_data['name']
        country_name = weather_data['sys']['country']
        wind = weather_data['wind']['speed']
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        weather_condtion = weather_data['weather'][0]['main']
        weather_description = weather_data['weather'][0]['description']

        # Calculate local time
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        find = TimezoneFinder()
        result = find.timezone_at(lng=location.longitude, lat=location.latitude)

        city_timezone = pytz.timezone(result)
        local_time = datetime.now(city_timezone)
        current_time = local_time.strftime("%I:%M %p")

        # Update text labels
        city_start.config(text=f"{city_name}, {country_name}")
        clock.config(text=current_time)
        temp_start.config(text=f"{temperature}°F")
        feels_start.config(text=f"FEELS LIKE:{feels_like}°F")
        wind_start.config(text=f"WIND:{wind} MPH")
        humidity_start.config(text=f"HUMIDITY: {humidity}%")
        weather_conditiontext.config(text =f"{weather_condtion}")
        weather_start.config(text=f"WEATHER:{weather_description.title()}")

        # Display textual weather conditions
        if weather_condtion == "Clear":
            weather_icon_label.config(text="☀️ Sunny", fg="yellow")
        elif weather_condtion == "Clouds":
            weather_icon_label.config(text="☁️ Cloudy", fg="gray")
        elif weather_condtion == "Rain":
            weather_icon_label.config(text="🌧️ Rainy", fg="blue")
        elif weather_condtion == "Snow":
            weather_icon_label.config(text="❄️ Snowy", fg="lightblue")
        elif weather_condtion == "Drizzle":
            weather_icon_label.config(text="🌦️ Drizzle", fg="blue")
        elif weather_condtion == "Thunderstorm":
            weather_icon_label.config(text="⛈️ Thunderstorm", fg="purple")
        elif weather_condtion == "Mist":
            weather_icon_label.config(text="🌫️ Misty", fg="white")
        else:
            weather_icon_label.config(text="🌡️ Unknown", fg="red")
    else:
        messagebox.showerror("Error", weather_data["message"])

        
def show_forecast():
    city = textfield.get()
    api_key = '27813a1f3eb806c48f81c63fe6e371af  # Replace with your actual API key'

    # Use OpenWeatherMap Geocoding API to get latitude and longitude of the city
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']

        # Use OneCall API for forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=imperial&appid={api_key}"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    print(forecast_data)  # Debugging line to inspect the structure

    if 'daily' in forecast_data:  # Check if 'daily' exists in the response
            # Clear the forecast frame
            for widget in forecast_frame.winfo_children():
                widget.destroy()

            Label(forecast_frame, text="7-Day Forecast", font=("Helvetica", 20, "bold"), bg="#FFA500", fg="white").pack(pady=10)

            # Display forecast data
            for day in forecast_data['daily']:
                dt = datetime.fromtimestamp(day['dt'])
                day_name = dt.strftime('%A')
                temp_min = day['temp']['min']
                temp_max = day['temp']['max']
                description = day['weather'][0]['description'].title()

                forecast_label = Label(forecast_frame, 
                                       text=f"{day_name}: {description}, High: {temp_max:.1f}°F, Low: {temp_min:.1f}°F",
                                       font=("Helvetica", 15), bg="#FFA500", fg="white")
                forecast_label.pack()
    else:
            messagebox.showerror("Error", "Forecast data not available in response.")
 


# Main Window
root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Search field and button
textfield = tk.Entry(root, justify="center", width=17, font=("Helvetica", 25, "bold"), bg="#FFA500", border=0, fg="white")
textfield.place(x=300, y=30)
textfield.focus()
root.bind('<Return>', get_weather)

search_button = Button(root, text="Search", borderwidth=0, cursor="hand2", bg="#FFA500", fg="white", font=("Helvetica", 15), command=get_weather)
search_button.place(x=620, y=30)

forecast_button = Button(root, text="7-Day Forecast", borderwidth=0, cursor="hand2", bg="#FFA500", fg="white", font=("Helvetica", 15), command=show_forecast)
forecast_button.place(x=620, y=45)
# Weather data labels
city_start = Label(root, font=("arial", 35, "bold"), bg="#FFA500")
city_start.place(x=30, y=90)

clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=160)

temp_start = Label(root, text="...", font=("Comic Sans", 40, "bold"), bg="#FFA500")
temp_start.place(x=550, y= 200)

feels_start = Label(root, text="...", font=("Comic Sans", 20, "bold"), bg="#FFA500")
feels_start.place(x=550, y=300)

wind_start = Label(root, text="...", font=("Comic Sans", 15, "bold"), bg="#FFA500")
wind_start.place(x=20, y=430)

humidity_start = Label(root, text="...", font=("Comic Sans", 15, "bold"), bg="#FFA500")
humidity_start.place(x=300, y=430)

weather_conditiontext = Label(root, text="...", font=("Comic Sans", 25, "bold"), bg="#FFA500")
weather_conditiontext.place(x=550, y=120)

weather_start = Label(root, text="...", font=("Comic Sans", 15, "bold"), bg="#FFA500")
weather_start.place(x=600, y=430)

weather_icon_label = Label(root, text="...", font=("Helvetica", 30), bg="#FFA500")
weather_icon_label.place(x=200, y=180)

forecast_frame = Frame(root, bg="#FFA500", width=800, height=200)
forecast_frame.place(x=50, y=500)

root.mainloop()

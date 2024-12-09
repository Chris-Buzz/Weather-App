import requests
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)


def get_weather(event = None):
    city = textfield.get()
    # Get API key from OpenWeatherMap (replace YOUR_API_KEY with your actual key)
    api_key = "27813a1f3eb806c48f81c63fe6e371af"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=imperial"

   
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
            # Extract required data
            city_name = weather_data['name']
            country_name = weather_data['sys']['country']
            timezone_offset = weather_data['timezone']
            wind = weather_data['wind']['speed']
            temperature = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            weather_condtion = weather_data['weather'][0]['main']
            weather_description = weather_data['weather'][0]['description']

            # Calculate local time
            geolocator = Nominatim(user_agent = "geoapiExercises")
            location = geolocator.geocode(city)
            find = TimezoneFinder()
            result = find.timezone_at(lng = location.longitude, lat = location.latitude)

            city_entered  = pytz.timezone(result)
            local_time = datetime.now(city_entered)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text = current_time)
            time.config(text = "CURRENT WEATHER")
            
            # Update labels with data
            city_start.config(text=f"{city_name}, {country_name}")
            time_label.config(text=f"{local_time}")
            temp_start.config(text=f"{temperature}°F")
            feels_start.config(text=f"{feels_like}°F")
            wind_start.config(text=f"{wind} MPH")
            humidity_start.config(text=f"{humidity}%")
            weather_start.config(text=f"{weather_description.title()}")

            if weather_condition == "Clear":
                icon_path = "icons/sunny.png"
            elif weather_condition == "Clouds":
                icon_path = "icons/cloudy.png"
            elif weather_condition == "Rain":
                icon_path = "icons/rainy.png"
            elif weather_condition == "Snow":
                icon_path = "icons/snowy.png"
            elif weather_condition == "Drizzle":
                icon_path = "icons/drizzle.png"
            elif weather_condition == "Thunderstorm":
                icon_path = "icons/thunderstorm.png"
            elif weather_condition == "Mist":
                icon_path = "icons/mist.png"
            else:
                icon_path = "icons/default.png"  # Default icon if condition not matched

            weather_icon_image = PhotoImage(file=icon_path)
            icon_label.config(image=weather_icon_image)
            icon_label.image = weather_icon_image
        
    else:
            messagebox.showerror("Error", weather_data["message"])



# Search field and button
Search_image = PhotoImage(file = "search.png")
myimage = Label (image = Search_image)
myimage.place(x=20,y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("Helvetica", 25, "bold"), bg="#FFA500", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()


root.bind('<Return>', get_weather)

#Search Icon
search_icon = PhotoImage(file="search_icon.png")  # Replace with your actual file path
search_button = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#FFA500", command = get_weather)
search_button.place(x=400, y=34)

#Logo
logo_image = PhotoImage(file="logo.png")  # Replace with your actual file path
logo = Label(image=logo_image)
logo.place(x=150, y=100)

#Text box
Text_box = PhotoImage(file = "box.png")
box_image = Label(image = Text_box)
box_image.pack(padx=5,pady=5,side=BOTTOM)

#time
city_start = Label( font = ("arial",40,"bold"),bg ="#FFA500")
city_start.place(x =30, y = 100)
time = Label(root, font = ("arial", 15, "bold"))
time.place(x = 30, y =130)
clock = Label(root, font =("Helvetica", 20))
clock.place(x=30, y=160)

# Labels for weather data

temp_label = Label(root, text = "TEMPERATURE" ,font=("Helvetica", 15), fg="white", bg="#FFA500")
temp_label.place(x=230, y=400,)

feels_like_label = Label(root, text = "FEELS LIKE",font=("Helvetica", 15), fg="white", bg="#FFA500")
feels_like_label.place(x=300, y=400)

wind_label =Label(root, text = "WIND ", font=("Helvetica", 15), fg="white", bg="#FFA500")
wind_label.place(x = 380,y =400)

humidity_label = Label(root, text ="HUMIDITY" ,font=("Helvetica", 15), fg="white", bg="#FFA500")
humidity_label.place(x=450, y=400)

weather_label = Label(root, text = "WEATHER DESCRIPTION", font=("Helvetica", 15), fg="white", bg="#FFA500")
weather_label.place(x=550, y=400)




temp_start = Label(text = "...", font = ("arial",50,"bold"),bg ="#FFA500")
temp_start.place(x =400, y = 150)

feels_start = Label(text = "...", font=("arial",20,"bold"),bg ="#FFA500")
feels_start.place(x =330, y = 430)

wind_start = Label(text = "...", font=("arial",20,"bold"),bg ="#FFA500")
wind_start.place(x =410, y = 430)

humidity_start = Label(text = "...", font=("arial",20,"bold"),bg ="#FFA500")
humidity_start.place(x =480, y = 430)

weather_start = Label(text = "...", font=("arial",20,"bold"),bg ="#FFA500")
weather_start.place(x =580, y = 430)




                                
root.mainloop()

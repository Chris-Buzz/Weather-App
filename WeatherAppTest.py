import requests
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

api_key = "27813a1f3eb806c48f81c63fe6e371af"
saved_cities = []
max_amount = 10

def get_weather():
    city = textfield.get()
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=imperial"

    response = requests.get(complete_url)
    weather_data = response.json()

    def addCity():
        global max_amount
        city = textfield.get()
        if city not in saved_cities and len(saved_cities) < max_amount:
            saved_cities.append(city)

            # Create a button for the saved city
            saved_city = Frame(saved_city_frame, bg="#FFA500")
            saved_city.pack(side=TOP, fill=BOTH, padx=5, pady=5)

            def select_city():
                textfield.delete(0, "end")
                textfield.insert(0, city)
                get_weather()

            def remove_city():
                saved_cities.remove(city)
                saved_city.destroy()


            Button(saved_city, text=city, font=("Helvetica", 10), bg="#FFA500", fg="white", justify="left", command=select_city).pack()
            Button(saved_city, text="❌",font=("Helvetica", 10, "bold"), bg="#FF6347", fg="white", command=remove_city).pack(side=LEFT, padx=5)
        elif city in saved_cities:
            messagebox.showerror("Error", "City already added to favorites")
        elif len(saved_cities) >= max_amount:
            messagebox.showerror("Error", f"Limit of {max_amount} saved cities reached")

    save_button = Button(root, text="Save City", bg ="#FFA500", command=addCity)
    save_button.place(x=820, y=30)
    
    

    if weather_data['cod'] == 200:
        city_name = weather_data['name']
        country_name = weather_data['sys']['country']
        wind = weather_data['wind']['speed']
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        weather_condtion = weather_data['weather'][0]['main']
        weather_description = weather_data['weather'][0]['description']

        
        geolocator = Nominatim(user_agent="WeatherApp")
        location = geolocator.geocode(city)
        find = TimezoneFinder()
        result = find.timezone_at(lng=location.longitude, lat=location.latitude)

        city_timezone = pytz.timezone(result)
        local_time = datetime.now(city_timezone)
        current_time = local_time.strftime("%I:%M %p")

      
        city_start.config(text=f"{city_name}, {country_name}")
        clock.config(text=current_time)
        temp_start.config(text=f"{temperature}°F")
        feels_start.config(text=f"FEELS LIKE:{feels_like}°F")
        wind_start.config(text=f"WIND:{wind} MPH")
        humidity_start.config(text=f"HUMIDITY: {humidity}%")
        weather_conditiontext.config(text =f"{weather_condtion}")
        weather_start.config(text=f"WEATHER:{weather_description.title()}")
 
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
        

#Display 5 day forecast
    def show_forecast(city_name):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        req = requests.get(url)
        data = req.json()

        name = data['name']
        lon = data['coord']['lon']
        lat = data['coord']['lat']

        url2 = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial'
        req2 = requests.get(url2)
        data2 = req2.json()

        for widget in forecast_frame.winfo_children():
            widget.destroy()
        
        Label(forecast_frame, text = "5-Day Forecast", font = ("Comic Sans", 20, "bold"), bg = "#FFA500")

        temps = []
        winds = []
        gusts = []
        max_temps = []
        min_temps = []
        max_winds = []
        min_winds = []
        max_gusts = []
        min_gusts = []
        humidity = []
        day_descriptions = []
        night_descriptions = []
        dates = []

        today = datetime.now().date().isoformat()
        current_day = None  

        for entry in data2['list']:
            date_txt = entry['dt_txt']
            hour = int(date_txt.split(" ")[1].split(":")[0])
            day = date_txt.split(" ")[0]

            if day == today:
                continue

            if current_day is not None and day != current_day:
                if temps:
                    max_temps.append(max(temps))
                    min_temps.append(min(temps))
                    temps = []
                if winds:
                    max_winds.append(max(winds))
                    min_winds.append(min(winds))
                    winds =[]
                if gusts:
                    max_gusts.append(max(gusts))
                    min_gusts.append(min(gusts))
                    gusts = []

            current_day = day

            
            if hour <= 21:
                temps.append(entry['main']['temp'])
                winds.append(entry['wind']['speed'])
                gusts.append(entry['wind']['gust'])

            if hour == 0 :  
                    humidity.append(entry['main']['humidity'])
                    day_descriptions.append(entry['weather'][0]['main'] + ": " + entry['weather'][0]['description'])
                    dates.append(current_day)
            elif hour == 12:
                if 'weather' in entry and len(entry['weather']) > 0:
                    night_descriptions.append(entry['weather'][0]['main'] + ": " + entry['weather'][0]['description'])
                else:
                    night_descriptions.append("No data available")

        if temps:
            max_temps.append(max(temps))
            min_temps.append(min(temps))
        if winds:
            max_winds.append(max(winds))
            min_winds.append(min(winds))
        if gusts:
            max_gusts.append(max(gusts))
            min_gusts.append(min(gusts))

        def get_day_of_week(date_str):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%A')

        Label(forecast_frame, text=f"5-Day Forecast for {city_name}", font=("Helvetica", 16, "bold"), bg="#FFA500", fg="white").pack(pady=10)
        
        for day in range(len(dates)):
                day_frame = Frame(forecast_frame, bg="#FFA500", pady=10, padx=10, relief=RIDGE, bd=2)
                day_frame.pack(side = LEFT, expand = True, fill = BOTH ,  padx = 5, pady = 5)

                date = dates[day]
                weekDay = get_day_of_week(date)

                forecast_text = f"""
        {weekDay} - {date}\n
        High: {max_temps[day]:,.0f}°F  |  Low: {min_temps[day]:,.0f}°F
        Wind: {min_winds[day]:,.0f} - {max_winds[day]:,.0f} MPH
        Gusts: {min_gusts[day]:,.0f} - {max_gusts[day]:,.0f} MPH
        Humidity: {humidity[day]:,.0f}%
        Day Conditions:
        {day_descriptions[day]}
        Night conditions:
        {night_descriptions[day]}
                """

                Label(day_frame, text=forecast_text, font=("Helvetica", 10), bg="#FFA500", fg="white", justify="left").pack()



    def outfit_inspo():

        if weather_condtion == "Clear":
           if temperature > 80:
               print("Top: Short sleeves, Bottom: Shorts")
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
        
#call forecast when weather is called
    show_forecast(city)
    



root = Tk()
root.title("Weather App")
root.geometry("1000x1000+300+200")
root.resizable(False, False)

textfield = tk.Entry(root, justify="center", width=17, font=("Helvetica", 25, "bold"), bg="#FFA500", border=0, fg="white")
textfield.place(x=300, y=30)
textfield.focus()
root.bind('<Return>', get_weather)


search_button = Button(root, text="Search", borderwidth=0, cursor="hand2", bg="#FFA500", fg="white", font=("Helvetica", 15), command=get_weather)
search_button.place(x=620, y=30)

forecast_frame = Frame(root, bg="white", width = 1000,height = 650)
forecast_frame.place(x = 0, y = 600)
for i in range(5):
    forecast_frame.columnconfigure(i, weight=1)

saved_city_frame = Frame(root, bg="white", width = 300,height = 500)
saved_city_frame.place(x = 800, y = 50)

Label(saved_city_frame, text = "Saved Cities",font=("Helvetica", 14, "bold"), bg="#FFA500", fg="white").pack(pady=10) 

city_start = Label(root, font=("arial", 35, "bold"), bg="#FFA500")
city_start.place(x=30, y=90)

clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=160)

temp_start = Label(root, text="...", font=("Comic Sans", 40, "bold"), bg="#FFA500")
temp_start.place(x=550, y= 200)

feels_start = Label(root, text="...", font=("Comic Sans", 20, "bold"), bg="#FFA500")
feels_start.place(x=400, y=300)

wind_start = Label(root, text="...", font=("Comic Sans", 15, "bold"), bg="#FFA500")
wind_start.place(x=20, y=430)

humidity_start = Label(root, text="...", font=("Comic Sans", 15, "bold"), bg="#FFA500")
humidity_start.place(x=200, y=430)

weather_conditiontext = Label(root, text="...", font=("Comic Sans", 25, "bold"), bg="#FFA500")
weather_conditiontext.place(x=500, y=120)

weather_start = Label(root, text="...", font=("Comic Sans", 15, "bold"), bg="#FFA500")
weather_start.place(x=400, y=430)

weather_icon_label = Label(root, text="...", font=("Helvetica", 30), bg="#FFA500")
weather_icon_label.place(x=200, y=180)


root.mainloop()

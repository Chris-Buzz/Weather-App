import requests
from datetime import datetime, timedelta

api_key = "your_api_key_here"
city_name = input("Enter city: ")


url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
req = requests.get(url)
data = req.json()

name = data['name']
lon = data['coord']['lon']
lat = data['coord']['lat']

url2 = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial'
req2 = requests.get(url2)
data2 = req2.json()

print(data2)

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
            night_descriptions.append(entry['weather'][0]['main'] + ": " + entry['weather'][0]['description'])

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

print(f"\n[{name} - 5-Day Forecast]\n")
for day in range(len(dates)):
    date = dates[day]
    weekDay = get_day_of_week(date)
    
    if day == 0:
        print(f"\nTomorrow - {date} -  {weekDay}\n")
    else:
        print(f"\n{date} - {weekDay}\n")


    print(f"Temperature:\nHigh: {max_temps[day]:,.0f}°F\nLow: {min_temps[day]:,.0f}°F")
    print(f"\nWinds: {min_winds[day]:,.0f} - {max_winds[day]:,.0f} MPH")
    print(f"Gusts: {min_gusts[day]:,.0f} - {min_gusts[day]:,.0f} MPH")
    print(f"Humidity: {humidity[day]:,.0f}")
    print(f"\nDay Conditions: {day_descriptions[day]}\n")
    print(f"Night Conditions: {night_descriptions[day]}")

                

    


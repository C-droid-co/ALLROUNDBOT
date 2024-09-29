import requests

API_KEY = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key

@client.on(events.NewMessage(pattern='/weather (.+)'))
async def weather(event):
    location = event.pattern_match.group(1)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temperature = main['temp']
        humidity = main['humidity']
        wind_speed = data['wind']['speed']
        
        weather_info = (
            f"Weather in {location}:\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Description: {weather_desc.capitalize()}\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        
        await event.respond(weather_info)
    else:
        await event.respond("Location not found. Please check the spelling and try again.")

import requests

# Replace 'your_api_key' with your actual API key
API_KEY = 'your_api_key'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

@client.on(events.NewMessage(pattern='!weather (.+)'))
async def get_weather(event):
    city_name = event.message.text.split(maxsplit=1)[1]
    complete_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data['cod'] != 200:
        await event.respond("City not found.")
        return

    main = data['main']
    wind = data['wind']
    weather_description = data['weather'][0]['description']

    weather_report = (
        f"Weather in {city_name}:\n"
        f"Temperature: {main['temp']}°C\n"
        f"Humidity: {main['humidity']}%\n"
        f"Description: {weather_description.capitalize()}\n"
        f"Wind Speed: {wind['speed']} m/s"
    )
    await event.respond(weather_report)

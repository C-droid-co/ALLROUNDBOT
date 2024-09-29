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

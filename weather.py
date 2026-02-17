import requests

def get_system_location():
    """Detects system city based on IP"""
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            return data.get('city', 'Mumbai') # Fallback to Mumbai
    except:
        pass
    return "Mumbai"

def get_coordinates(city_name):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                return result['latitude'], result['longitude'], result['name']
    except Exception as e:
        print(f"Geo-coding error: {e}")
    return None, None, None

def get_weather_data(city_name):
    """
    Returns a dictionary with raw weather data for UI or logic usage:
    {
        "temp": 24,
        "condition": "Cloudy", # or code
        "wind": 12,
        "city": "Mumbai",
        "error": None
    }
    """
    lat, lon, name = get_coordinates(city_name)
    if not lat:
        return {"error": f"I couldn't find the location {city_name}."}
    
    try:
        # Requesting weather code as well for icons
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            curr = data.get('current_weather', {})
            temp = curr.get('temperature', 'N/A')
            wind = curr.get('windspeed', 'N/A')
            # detailed condition mapping could go here, for now passing raw code if needed or just simple text
            # OpenMeteo weather codes: 0=Clear, 1-3=Cloudy, etc.
            # We can just return the object and let the UI or main logic parse it
            return {
                "temp": temp,
                "wind": wind,
                "city": name,
                "weathercode": curr.get('weathercode', 0),
                "error": None
            }
    except Exception as e:
        return {"error": "I couldn't fetch the weather data."}
    
    return {"error": "Weather data unavailable."}

def get_weather(city_name):
    """Legacy wrapper for voice response"""
    data = get_weather_data(city_name)
    if data.get("error"):
        return data["error"]
    
    return f"Current weather in {data['city']}: {data['temp']} degrees Celsius, wind speed {data['wind']} kilometers per hour."

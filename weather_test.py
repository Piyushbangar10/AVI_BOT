import weather

print("Detecting location...")
loc = weather.get_system_location()
print(f"Detected City: {loc}")

print("Fetching weather for detected city...")
data = weather.get_weather_data(loc)
print(f"Weather Data: {data}")

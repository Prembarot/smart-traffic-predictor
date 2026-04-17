import requests

WEATHER_API_KEY = "05f168a277005e12e4f1671118eb6390"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_main = data["weather"][0]["main"]

    except:
        # fallback dummy data
        temp = 30
        humidity = 70
        weather_main = "Clear"

    # encoding
    weather = 0 if weather_main == "Clear" else 1
    rain = 1 if weather_main == "Rain" else 0

    return temp, humidity, weather, rain


ORS_API_KEY = "KGvFHoQnCtIR3BPZPk1cRcqWHUJIYGmv"


def get_traffic_time(start_lat, start_lon, end_lat, end_lon):
    try:
        import requests

        url = "https://api.openrouteservice.org/v2/directions/driving-car"

        headers = {
            "Authorization": f"Bearer {ORS_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [
                [start_lon, start_lat],
                [end_lon, end_lat]
            ]
        }

        response = requests.post(url, json=body, headers=headers)
        data = response.json()

        if "routes" not in data:
            raise Exception(data)

        return data["routes"][0]["summary"]["duration"] / 60

    except Exception as e:
        print("⚠️ ORS failed, using fallback:", e)

        # 🔥 SMART FALLBACK (distance-based)
        from math import sqrt

        distance = sqrt((end_lat - start_lat)**2 + (end_lon - start_lon)**2)

        # assume avg speed → 40 km/h
        time = distance * 111 / 40 * 60

        return round(time, 2)
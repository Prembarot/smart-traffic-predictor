from fastapi import FastAPI
from dataset.smart_traffic import predict_traffic
from geopy.distance import geodesic
import requests
import datetime
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
@app.get("/")
def home():
    return {"message": "🚗 Smart Traffic Predictor API is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DISTANCE FUNCTION
# =========================
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


# =========================
# API KEY
# =========================
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# =========================
# MAIN API
# =========================
@app.post("/predict-real")
def predict_real(city: str, start_lat: float, start_lon: float, end_lat: float, end_lon: float):

    try:
        # =========================
        # WEATHER API (SAFE)
        # =========================
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            weather_res = requests.get(weather_url)
            weather_data = weather_res.json()

            if weather_res.status_code == 200:
                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                rain = 1 if "rain" in weather_data else 0
                weather = 1
            else:
                raise Exception("Weather API failed")

        except:
            # 🔥 fallback if API fails
            temp = 30
            humidity = 60
            rain = 0
            weather = 1

        # =========================
        # TIME FEATURES
        # =========================
        now = datetime.datetime.now()
        hour = now.hour
        day = now.weekday()

        # =========================
        # DISTANCE
        # =========================
        distance = calculate_distance(start_lat, start_lon, end_lat, end_lon)

        # =========================
        # ML PREDICTION
        # =========================
        ml_time = predict_traffic(hour, day, weather, rain, temp, humidity, distance)

        # =========================
        # 🔥 REAL TIME (NO API - SAFE)
        # =========================
        avg_speed = 50  # km/h
        traffic_factor = 1.3 if rain else 1.0

        real_time = (distance / avg_speed) * 60 * traffic_factor  # minutes

        # =========================
        # FINAL RESPONSE
        # =========================
        return {
            "ml_predicted_time": round(ml_time, 2),
            "real_traffic_time": round(real_time, 2),
            "distance_km": round(distance, 2),
            "weather_temp": temp,
            "humidity": humidity
        }

    except Exception as e:
        return {"error": str(e)}

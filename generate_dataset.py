import pandas as pd
import random

data = []

for _ in range(1000):  # generate 1000 rows

    hour = random.randint(0, 23)
    day = random.randint(0, 6)
    weather = random.randint(0, 2)  # 0=clear,1=cloudy,2=rainy
    rain = random.randint(0, 1)
    temp = random.randint(20, 40)
    humidity = random.randint(30, 90)

    # 🔥 NEW FEATURE
    distance = round(random.uniform(1, 50), 2)  # km

    # 🎯 REALISTIC FORMULA (important)
    base_speed = 40  # km/h
    traffic_factor = 1 + (hour / 24) + (rain * 0.5)

    travel_time = (distance / base_speed) * 60 * traffic_factor  # minutes

    data.append([hour, day, weather, rain, temp, humidity, distance, round(travel_time, 2)])

df = pd.DataFrame(data, columns=[
    "hour","day","weather","rain","temp","humidity","distance","travel_time"
])

df.to_csv("processed_data.csv", index=False)

print("✅ Dataset generated successfully!")
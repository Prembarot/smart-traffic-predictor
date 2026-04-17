import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("processed_data.csv")

# =========================
# FEATURES (UPDATED)
# =========================
X = df[['hour', 'day', 'weather', 'rain', 'temp', 'humidity', 'distance']]
y = df['travel_time']

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# =========================
# MODEL
# =========================
model = RandomForestRegressor()
model.fit(X_train, y_train)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "traffic_model.pkl")

print("✅ Model trained and saved!")

# =========================
# PREDICT FUNCTION
# =========================
def predict_traffic(hour, day, weather, rain, temp, humidity, distance):
    model = joblib.load("traffic_model.pkl")

    prediction = model.predict([[
        hour, day, weather, rain, temp, humidity, distance
    ]])

    return round(prediction[0], 2)
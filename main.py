from dataset.smart_traffic import train_model, predict_traffic

# Train model (will also show metrics + graph)
train_model("data/raw_data.csv")

print("\nEnter Traffic Details:")

hour = int(input("Hour (0-23): "))
day = int(input("Day (1=Mon, ..., 7=Sun): "))
weather = int(input("Weather (0=Clear, 1=Clouds, 2=Rain): "))
rain = int(input("Rain (0=No, 1=Yes): "))
temp = float(input("Temperature (°C): "))
humidity = int(input("Humidity (%): "))

input_data = [hour, day, weather, rain, temp, humidity]

prediction = predict_traffic(input_data)

print(f"\n🚦 Predicted Travel Time: {prediction:.2f} minutes")
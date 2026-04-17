from dataset.smart_traffic import predict_traffic

# Dummy routes (later replace with API)
routes = [
    {"route": "Route A", "distance": 10},
    {"route": "Route B", "distance": 12},
    {"route": "Route C", "distance": 8},
]

def get_best_route(hour, day, weather, rain, temp, humidity):
    best_route = None
    min_time = float("inf")

    for r in routes:
        input_data = [hour, day, weather, rain, temp, humidity]
        predicted_time = predict_traffic(input_data)

        # Adjust using distance (simple logic)
        total_time = predicted_time + r["distance"]

        if total_time < min_time:
            min_time = total_time
            best_route = r["route"]

    return best_route, min_time
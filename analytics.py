def traffic_density(vehicle_count):

    if vehicle_count <= 10:
        return "LOW"

    elif vehicle_count <= 25:
        return "MEDIUM"

    elif vehicle_count <= 50:
        return "HIGH"

    else:
        return "CRITICAL"
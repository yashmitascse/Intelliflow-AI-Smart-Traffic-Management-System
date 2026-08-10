def get_signal_time(vehicle_count):

    if vehicle_count <= 10:
        return 15

    elif vehicle_count <= 25:
        return 30

    elif vehicle_count <= 50:
        return 45

    else:
        return 60
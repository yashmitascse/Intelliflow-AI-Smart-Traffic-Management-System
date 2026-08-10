def count_vehicles(ids):
    if ids is None:
        return 0

    return len(set(ids))
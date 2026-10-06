import math

CAMPUS_CENTER = (31.579761694261773, 74.35494969618985)

# Bounding box approximating a 5 km radius around the campus center
CAMPUS_BOUNDS = {
    "south": 31.5348,
    "north": 31.6247,
    "west":  74.3022,
    "east":  74.4077,
}


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 3)


def is_inside_campus(lat: float, lon: float) -> bool:
    if lat is None or lon is None:
        return False
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (ValueError, TypeError):
        return False
    return (
        CAMPUS_BOUNDS["south"] <= lat_f <= CAMPUS_BOUNDS["north"]
        and CAMPUS_BOUNDS["west"] <= lon_f <= CAMPUS_BOUNDS["east"]
    )


def compute_distance(pickup_lat: float, pickup_lon: float, dropoff_lat: float, dropoff_lon: float) -> float:
    return haversine(float(pickup_lat), float(pickup_lon), float(dropoff_lat), float(dropoff_lon))

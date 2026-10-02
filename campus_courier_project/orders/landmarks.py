from typing import Optional, Tuple
from orders.utils import haversine

CAMPUS_LANDMARKS = [
    # Main gates & administrative
    { 'name': 'Main Gate', 'lat': 31.57976, 'lon': 74.35495, 'category': 'gate' },
    { 'name': 'Gate 3', 'lat': 31.57843, 'lon': 74.35886, 'category': 'gate' },
    { 'name': 'Admin Block', 'lat': 31.57699, 'lon': 74.35444, 'category': 'administrative' },
    { 'name': 'VC Office', 'lat': 31.57750, 'lon': 74.35500, 'category': 'administrative' },

    # Academic
    { 'name': 'Main Library', 'lat': 31.57811, 'lon': 74.35502, 'category': 'academic' },
    { 'name': 'Computer Science Dept', 'lat': 31.57900, 'lon': 74.35600, 'category': 'academic' },
    { 'name': 'Electrical Engineering Dept', 'lat': 31.57850, 'lon': 74.35550, 'category': 'academic' },
    { 'name': 'Mechanical Engineering Dept', 'lat': 31.57780, 'lon': 74.35620, 'category': 'academic' },
    { 'name': 'Civil Engineering Dept', 'lat': 31.57720, 'lon': 74.35580, 'category': 'academic' },
    { 'name': 'Chemical Engineering Dept', 'lat': 31.57680, 'lon': 74.35520, 'category': 'academic' },
    { 'name': 'Architecture Dept', 'lat': 31.57650, 'lon': 74.35650, 'category': 'academic' },
    { 'name': 'Petroleum & Gas Dept', 'lat': 31.57920, 'lon': 74.35480, 'category': 'academic' },
    { 'name': 'Metallurgy Dept', 'lat': 31.57750, 'lon': 74.35680, 'category': 'academic' },
    { 'name': 'Industrial & Manufacturing Dept', 'lat': 31.57700, 'lon': 74.35700, 'category': 'academic' },
    { 'name': 'Chemical Engineering Lab Block', 'lat': 31.57670, 'lon': 74.35540, 'category': 'academic' },
    { 'name': 'Electrical Engineering Lab Block', 'lat': 31.57860, 'lon': 74.35560, 'category': 'academic' },
    { 'name': 'Mechatronics Dept', 'lat': 31.57790, 'lon': 74.35630, 'category': 'academic' },
    { 'name': 'Transportation Engineering Dept', 'lat': 31.57740, 'lon': 74.35440, 'category': 'academic' },
    { 'name': 'Architectural Engineering Dept', 'lat': 31.57660, 'lon': 74.35660, 'category': 'academic' },
    { 'name': 'City & Regional Planning Dept', 'lat': 31.57640, 'lon': 74.35640, 'category': 'academic' },
    { 'name': 'IB&M (Business School)', 'lat': 31.57940, 'lon': 74.35510, 'category': 'academic' },
    { 'name': 'Physics Dept', 'lat': 31.57910, 'lon': 74.35520, 'category': 'academic' },
    { 'name': 'Chemistry Dept', 'lat': 31.57900, 'lon': 74.35530, 'category': 'academic' },
    { 'name': 'Mathematics Dept', 'lat': 31.57890, 'lon': 74.35540, 'category': 'academic' },

    # Hostels
    { 'name': 'Sir Syed Hall', 'lat': 31.58050, 'lon': 74.35590, 'category': 'hostel' },
    { 'name': 'Muhammad Bin Qasim Hall', 'lat': 31.58030, 'lon': 74.35680, 'category': 'hostel' },
    { 'name': 'Zubair Hall', 'lat': 31.58040, 'lon': 74.35590, 'category': 'hostel' },
    { 'name': 'Ali Mardan Hall', 'lat': 31.58050, 'lon': 74.35580, 'category': 'hostel' },
    { 'name': 'Sultan Mahmud Ghaznavi Hall', 'lat': 31.58090, 'lon': 74.35540, 'category': 'hostel' },
    { 'name': 'Faculty Hostel (RT Hostel)', 'lat': 31.58000, 'lon': 74.35650, 'category': 'hostel' },
    { 'name': 'Girls Hostel', 'lat': 31.58100, 'lon': 74.35750, 'category': 'hostel' },

    # Food & student life
    { 'name': 'Sports Cafeteria', 'lat': 31.58060, 'lon': 74.35580, 'category': 'food' },
    { 'name': 'Student Service Center (Male)', 'lat': 31.57880, 'lon': 74.35450, 'category': 'food' },
    { 'name': 'Student Service Center (Female)', 'lat': 31.57900, 'lon': 74.35400, 'category': 'food' },
    { 'name': 'Student Cafe (Main)', 'lat': 31.58000, 'lon': 74.35500, 'category': 'food' },
    { 'name': 'Faculty Cafe', 'lat': 31.57750, 'lon': 74.35510, 'category': 'food' },

    # Religious & sports
    { 'name': 'Central Jamia Mosque', 'lat': 31.57750, 'lon': 74.35600, 'category': 'religious' },
    { 'name': 'Junaid Jamshed Stadium', 'lat': 31.58100, 'lon': 74.35800, 'category': 'sports' },
    { 'name': 'Sports Complex / Gymnasium', 'lat': 31.58060, 'lon': 74.35580, 'category': 'sports' },
    { 'name': 'UET Grand Mosque', 'lat': 31.57850, 'lon': 74.35700, 'category': 'religious' },

    # Services
    { 'name': 'HBL Bank / ATM', 'lat': 31.57661, 'lon': 74.35463, 'category': 'service' },
    { 'name': 'Medical Center / Dispensary', 'lat': 31.57710, 'lon': 74.35410, 'category': 'service' },
    { 'name': 'Post Office', 'lat': 31.57720, 'lon': 74.35420, 'category': 'service' },
    { 'name': 'Transport Office', 'lat': 31.57730, 'lon': 74.35430, 'category': 'service' },
    { 'name': 'Buss Stand (Terminal)', 'lat': 31.57700, 'lon': 74.35400, 'category': 'service' },
]


def find_nearest_landmark(lat: float, lon: float, max_distance_m: float = 150.0) -> dict | None:
    """
    Return the closest landmark dict within max_distance_m meters,
    or None if no landmark is within that radius.
    Uses haversine() from orders.utils.
    Distances in meters = haversine() * 1000.
    """
    nearest = None
    min_dist = float('inf')
    for lm in CAMPUS_LANDMARKS:
        dist_m = haversine(lat, lon, lm['lat'], lm['lon']) * 1000.0
        if dist_m <= max_distance_m and dist_m < min_dist:
            min_dist = dist_m
            nearest = lm
    return nearest


def describe_location(lat: float, lon: float) -> tuple[str, str]:
    """
    Returns (label, source) where source is 'landmark' or 'coords'.
    If find_nearest_landmark returns a dict, label = landmark['name'], source = 'landmark'.
    Else label = f"{lat:.5f}, {lon:.5f}", source = 'coords'.
    """
    landmark = find_nearest_landmark(lat, lon)
    if landmark:
        return landmark['name'], 'landmark'
    return f"{lat:.5f}, {lon:.5f}", 'coords'

def landmarks_for_json() -> list[dict]:
    return [
        {
            'name': lm['name'],
            'lat': lm['lat'],
            'lon': lm['lon'],
            'category': lm['category']
        }
        for lm in CAMPUS_LANDMARKS
    ]

from typing import Optional, Tuple
from orders.utils import haversine

CAMPUS_LANDMARKS = [
    # Main gates & administrative
   # { 'name': 'Gate 0', 'lat': 31.57976, 'lon': 74.35495, 'category': 'gate' },
    { 'name': 'Gate 3', 'lat': 31.576839, 'lon': 74.356816, 'category': 'gate' },
    { 'name': 'Admin Block', 'lat': 31.577022, 'lon': 74.354821, 'category': 'administrative' },
    { 'name': 'VC Office', 'lat': 31.577301, 'lon': 74.355561, 'category': 'administrative' },

    # Academic
    { 'name': 'Main Library', 'lat': 31.578640, 'lon': 74.356333, 'category': 'academic' },
    { 'name': 'Computer Science Dept', 'lat': 31.578601, 'lon': 74.357650, 'category': 'academic' },
    { 'name': 'Electrical Engineering Dept', 'lat': 31.577156, 'lon': 74.356381, 'category': 'academic' },
    { 'name': 'Mechanical Engineering Dept', 'lat': 31.577843, 'lon': 74.358369, 'category': 'academic' },
    { 'name': 'Civil Engineering Dept', 'lat': 31.578774, 'lon': 74.357218, 'category': 'academic' },
    { 'name': 'Chemical Engineering Dept', 'lat': 31.579771, 'lon': 74.356150, 'category': 'academic' },
    { 'name': 'Architecture Dept', 'lat': 31.577898, 'lon': 74.355473, 'category': 'academic' },
    { 'name': 'Petroleum & Gas Dept', 'lat': 31.580101, 'lon': 74.356673, 'category': 'academic' },
    { 'name': 'Metallurgy Dept', 'lat': 31.580264, 'lon': 74.357550, 'category': 'academic' },
   # { 'name': 'Industrial & Manufacturing Dept', 'lat': 31.57700, 'lon': 74.35700, 'category': 'academic' },
    { 'name': 'Chemical Engineering Lab Block', 'lat': 31.580318, 'lon': 74.356386, 'category': 'academic' },
    #{ 'name': 'Electrical Engineering Lab Block', 'lat': 31.57860, 'lon': 74.35560, 'category': 'academic' },
    { 'name': 'Mechatronics Dept', 'lat': 31.577710, 'lon': 74.358603, 'category': 'academic' },
    { 'name': 'Transportation Engineering Dept', 'lat': 31.578837, 'lon': 74.357569, 'category': 'academic' },
    { 'name': 'Architectural Engineering Dept', 'lat': 31.578940, 'lon': 74.355884, 'category': 'academic' },
    { 'name': 'City & Regional Planning Dept', 'lat': 31.578939, 'lon': 74.355627, 'category': 'academic' },
    { 'name': 'IBM (Business School)', 'lat': 31.578595, 'lon': 74.353738, 'category': 'academic' },
    { 'name': 'Main Block(Physics Dept)', 'lat': 31.577967, 'lon': 74.359799, 'category': 'academic' },
    { 'name': 'Chemistry Dept', 'lat': 31.576999, 'lon': 74.352259, 'category': 'academic' },
    { 'name': 'Mathematics Dept', 'lat': 31.578506, 'lon': 74.358056, 'category': 'academic' },

    # Hostels
    { 'name': 'Sir Syed Hall', 'lat': 31.582189, 'lon': 74.351067, 'category': 'hostel' },
    { 'name': 'Iqbal Hall', 'lat': 31.582318, 'lon': 74.352019, 'category': 'hostel' },
    { 'name': 'Quaid-e-Azam Hall', 'lat': 31.580951, 'lon': 74.351266, 'category': 'hostel' },
    { 'name': 'Liaqat Hall', 'lat': 31.581081, 'lon': 74.352317, 'category': 'hostel' },
    { 'name': 'Mumtaz Hall', 'lat': 31.580880, 'lon': 74.352113, 'category': 'hostel' },
    { 'name': 'Muhammad Bin Qasim Hall', 'lat': 31.579315, 'lon': 74.352075, 'category': 'hostel' },
    { 'name': 'Zubair Hall', 'lat': 31.579386, 'lon': 74.352402, 'category': 'hostel' },
    { 'name': 'Edhi Hall', 'lat': 31.579226, 'lon': 74.351817, 'category': 'hostel' },
    { 'name': 'Sultan Mahmud Ghaznavi Hall', 'lat': 31.579420, 'lon': 74.353034, 'category': 'hostel' },
    { 'name': 'Tariq Hall', 'lat': 31.578497, 'lon': 74.352588, 'category': 'hostel' },
    { 'name': 'Khalid Hall', 'lat': 31.578489, 'lon': 74.352132, 'category': 'hostel' },
    { 'name': 'Ali Mardan Hall', 'lat': 31.578114, 'lon':  74.351649, 'category': 'hostel' },
    { 'name': 'Faculty Hostel (RT Hostel)', 'lat': 31.579056, 'lon': 74.359399, 'category': 'hostel' },
    { 'name': 'Ayesha Hall', 'lat': 31.578515, 'lon': 74.359693, 'category': 'hostel' },
    { 'name': 'New Girls Hostel', 'lat': 31.579234, 'lon': 74.361855, 'category': 'hostel' },
    { 'name': 'C Hall', 'lat': 31.579211, 'lon': 74.362051, 'category': 'hostel' },
    { 'name': 'Umer Hall', 'lat': 31.578749, 'lon': 74.362073, 'category': 'hostel' },
    { 'name': 'Khadija Hall', 'lat': 31.579125, 'lon': 74.360260, 'category': 'hostel' },

    # Food & student life
    { 'name': 'GSSC(Girls Service Centre)', 'lat': 31.578923, 'lon': 74.358245, 'category': 'food' },
    { 'name': 'SSC(Student Service Center)', 'lat': 31.578837, 'lon': 74.353418, 'category': 'food' },
    { 'name': 'Shopping Centre', 'lat': 31.579661, 'lon': 74.353279, 'category': 'food' },
    { 'name': 'Bhola Cafe', 'lat': 31.580613, 'lon': 74.354514, 'category': 'food' },
    { 'name': 'Annexe', 'lat': 31.577451, 'lon': 74.351722, 'category': 'food' },

    # Religious & sports
    { 'name': 'Central Jamia Mosque', 'lat': 31.578587, 'lon': 74.354979, 'category': 'religious' },
    { 'name': 'Junaid Jamshed Stadium', 'lat': 31.581076, 'lon': 74.354987, 'category': 'sports' },
    { 'name': 'Sports Complex / Gymnasium', 'lat': 31.581051, 'lon': 74.352946, 'category': 'sports' },
    { 'name': 'UET Grand Mosque', 'lat': 31.578437, 'lon': 74.355361, 'category': 'religious' },

    # Services
    { 'name': 'ATM', 'lat': 31.578719, 'lon': 74.356316, 'category': 'service' },
    { 'name': 'Medical Center / Dispensary', 'lat': 31.582288, 'lon': 74.353870, 'category': 'service' },
    { 'name': 'Post Office', 'lat': 31.579647, 'lon': 74.357728, 'category': 'service' },
    { 'name': 'Buss Stand(Terminal)', 'lat': 31.578765, 'lon': 74.354321, 'category': 'service' },
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

ITEM_TYPE_CODES = {
    'DOCUMENT': 0, 'FOOD': 1, 'ELECTRONICS': 2,
    'CLOTHING': 3, 'BOOKS': 4, 'OTHER': 5,
}

ITEM_TYPE_BONUS = {
    'DOCUMENT': 0, 'FOOD': 15, 'ELECTRONICS': 40,
    'CLOTHING': 5, 'BOOKS': 5, 'OTHER': 10,
}

def code_for(item_type_str: str) -> int:
    return ITEM_TYPE_CODES.get(item_type_str.upper(), 5)

PEAK_HOURS = {8, 9, 12, 13, 17, 18}

def is_peak_hour(hour: int) -> bool:
    return hour in PEAK_HOURS

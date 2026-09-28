import os
import joblib
from django.conf import settings
from ml_engine.item_types import code_for

_model = None
_model_path = settings.BASE_DIR / 'ml_engine' / 'fare_model.joblib'

def _load():
    global _model
    if _model is None:
        if not model_available():
            raise RuntimeError("Model not trained. Run: python manage.py train_fare_model")
        _model = joblib.load(_model_path)

def model_available() -> bool:
    return os.path.exists(_model_path)

def predict_fare(distance_km: float, weight_kg: float, hour: int, item_type: str) -> float:
    _load()
    peak_hour = 1 if hour in [8, 9, 12, 13, 17, 18] else 0
    is_food = 1 if item_type == 'FOOD' else 0
    is_electronics = 1 if item_type == 'ELECTRONICS' else 0
    is_clothing = 1 if item_type == 'CLOTHING' else 0
    is_books = 1 if item_type == 'BOOKS' else 0
    is_other = 1 if item_type == 'OTHER' else 0

    X = [[distance_km, weight_kg, peak_hour,
          is_food, is_electronics, is_clothing, is_books, is_other]]

    return round(float(_model.predict(X)[0]), 2)

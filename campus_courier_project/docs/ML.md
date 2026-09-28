# ML — Fare Prediction

## Goal
Predict a fair fare in PKR given order features. Runs as a management command that trains and saves a model. Inference runs synchronously in the request cycle (fast, <10ms).

## Model
`sklearn.linear_model.Ridge` (fallback: `LinearRegression`). Chosen for speed, interpretability, and no tuning overhead.

## Features

| Feature | Type | Range |
|---|---|---|
| distance_km | float | 0.1 – 10.0 |
| weight_kg | float | 0.1 – 20.0 |
| hour | int | 0 – 23 (Used for synthetic generation only) |
| item_type_code | int | 0 – 5 (Used for synthetic generation only) |
| peak_hour | int | 0 or 1 (1 if hour ∈ {8,9,12,13,17,18}) |
| is_food, is_electronics, is_clothing, is_books, is_other | int | 0 or 1 (one-hot, DOCUMENT is the reference) |

**Feature order**: [distance_km, weight_kg, peak_hour, is_food, is_electronics, is_clothing, is_books, is_other]

One-hot encoding and the peak_hour binary are required because the synthetic target is nonlinear in hour and item_type.
## Synthetic Data Formula (before training)

```
base          = 50
distance_term = 25 * distance_km
weight_term   = 10 * weight_kg
peak_surge    = 30 if hour in [8,9,12,13,17,18] else 0
item_bonus    = {'DOCUMENT': 0, 'FOOD': 15, 'ELECTRONICS': 40,
                 'CLOTHING': 5, 'BOOKS': 5, 'OTHER': 10}[item_type]
fare = base + distance_term + weight_term + peak_surge + item_bonus
fare += N(0, 15)
```

Generate 8000 samples. Train/test split 80/20. Report MAE.

## Files

```
ml_engine/
├── predictor.py
├── fare_model.joblib          # generated, gitignored
└── management/
    └── commands/
        └── train_fare_model.py
```

### `predictor.py`
```python
import joblib, os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_engine', 'fare_model.joblib')
_model = None

def _load():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_fare(distance_km, weight_kg, hour, item_type):
    peak_hour = 1 if hour in [8, 9, 12, 13, 17, 18] else 0
    is_food = 1 if item_type == 'FOOD' else 0
    is_electronics = 1 if item_type == 'ELECTRONICS' else 0
    is_clothing = 1 if item_type == 'CLOTHING' else 0
    is_books = 1 if item_type == 'BOOKS' else 0
    is_other = 1 if item_type == 'OTHER' else 0

    X = [[distance_km, weight_kg, peak_hour,
          is_food, is_electronics, is_clothing, is_books, is_other]]
    return float(_load().predict(X)[0])
```

## Training Command

```bash
python manage.py train_fare_model
```

Prints MAE and saves `fare_model.joblib`.

## Versioning
- Model file is versioned with a `ml_engine/fare_model.meta.json` recording: training date, sample count, MAE, feature list.
- Retrain when formula or features change.

## Not in v1
- DBSCAN hotspots
- Bid acceptance classifier
- Deep learning
- Online learning

import json
import numpy as np
from datetime import datetime
import joblib
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from django.core.management.base import BaseCommand
from django.conf import settings
from ml_engine.item_types import ITEM_TYPE_CODES, ITEM_TYPE_BONUS

class Command(BaseCommand):
    help = 'Train the fare prediction model'

    def handle(self, *args, **options):
        np.random.seed(42)
        n_samples = 8000

        distance_km = np.random.uniform(0.1, 10.0, n_samples)
        weight_kg = np.random.uniform(0.1, 20.0, n_samples)
        hour = np.random.randint(0, 24, n_samples)
        
        item_types = list(ITEM_TYPE_CODES.keys())
        chosen_items = np.random.choice(item_types, n_samples)
        item_type_code = np.array([ITEM_TYPE_CODES[it] for it in chosen_items])

        base = 50
        distance_term = 25 * distance_km
        weight_term = 10 * weight_kg
        
        peak_surge = np.zeros(n_samples)
        for i in range(n_samples):
            if hour[i] in [8, 9, 12, 13, 17, 18]:
                peak_surge[i] = 30
                
        item_bonus = np.array([ITEM_TYPE_BONUS[it] for it in chosen_items])
        
        noise = np.random.normal(0, 15, n_samples)
        
        fare = base + distance_term + weight_term + peak_surge + item_bonus + noise

        peak_hour = np.array([1 if h in [8, 9, 12, 13, 17, 18] else 0 for h in hour])
        is_food = np.array([1 if it == 'FOOD' else 0 for it in chosen_items])
        is_electronics = np.array([1 if it == 'ELECTRONICS' else 0 for it in chosen_items])
        is_clothing = np.array([1 if it == 'CLOTHING' else 0 for it in chosen_items])
        is_books = np.array([1 if it == 'BOOKS' else 0 for it in chosen_items])
        is_other = np.array([1 if it == 'OTHER' else 0 for it in chosen_items])

        X = np.column_stack((distance_km, weight_kg, peak_hour, is_food, is_electronics, is_clothing, is_books, is_other))
        y = fare

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        self.stdout.write(self.style.SUCCESS(f"Model trained successfully. MAE on test set: {mae:.2f}"))

        model_path = settings.BASE_DIR / 'ml_engine' / 'fare_model.joblib'
        meta_path = settings.BASE_DIR / 'ml_engine' / 'fare_model.meta.json'

        joblib.dump(model, model_path)

        meta_data = {
            "trained_at": datetime.now().isoformat(),
            "n_samples": n_samples,
            "mae": float(mae),
            "features": ["distance_km", "weight_kg", "peak_hour", "is_food",
                         "is_electronics", "is_clothing", "is_books", "is_other"]
        }

        with open(meta_path, 'w') as f:
            json.dump(meta_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Model and metadata saved to {model_path} and {meta_path}"))

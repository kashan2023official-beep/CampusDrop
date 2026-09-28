import json
import pytest
from ml_engine.predictor import predict_fare, model_available


@pytest.mark.skipif(not model_available(), reason="Trained fare model file missing")
def test_model_loads():
    """Trained fare prediction model loads and yields a positive numeric fare."""
    fare = predict_fare(distance_km=1.0, weight_kg=1.0, hour=12, item_type='DOCUMENT')
    assert isinstance(fare, float)
    assert fare > 0


@pytest.mark.skipif(not model_available(), reason="Trained fare model file missing")
def test_fare_increases_with_distance():
    """Predicted fare strictly increases when travel distance increases."""
    fare_short = predict_fare(distance_km=0.5, weight_kg=1.0, hour=12, item_type='DOCUMENT')
    fare_long = predict_fare(distance_km=3.0, weight_kg=1.0, hour=12, item_type='DOCUMENT')
    assert fare_long > fare_short


@pytest.mark.skipif(not model_available(), reason="Trained fare model file missing")
def test_fare_increases_with_weight():
    """Predicted fare strictly increases when package weight increases."""
    fare_light = predict_fare(distance_km=1.0, weight_kg=0.5, hour=12, item_type='DOCUMENT')
    fare_heavy = predict_fare(distance_km=1.0, weight_kg=5.0, hour=12, item_type='DOCUMENT')
    assert fare_heavy > fare_light


@pytest.mark.django_db
def test_predict_endpoint_validates_input(client, sender_user):
    """Predict fare API endpoint rejects invalid weights, distances, and item types."""
    client.force_login(sender_user)

    # Negative distance / out of range
    invalid_payload = {
        'distance_km': -5.0,
        'weight_kg': 1.0,
        'item_type': 'DOCUMENT',
    }
    response = client.post(
        '/api/predict-fare/',
        data=json.dumps(invalid_payload),
        content_type='application/json',
    )
    assert response.status_code == 400
    data = response.json()
    assert data.get('error') == 'invalid_input'
    assert 'distance_km' in data.get('fields', {})

    # Invalid item type
    invalid_type_payload = {
        'distance_km': 1.5,
        'weight_kg': 1.0,
        'item_type': 'INVALID_TYPE',
    }
    response2 = client.post(
        '/api/predict-fare/',
        data=json.dumps(invalid_type_payload),
        content_type='application/json',
    )
    assert response2.status_code == 400
    data2 = response2.json()
    assert 'item_type' in data2.get('fields', {})

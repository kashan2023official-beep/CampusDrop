import json
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from core.audit import log, client_ip
from ml_engine.predictor import predict_fare, model_available
from ml_engine.item_types import ITEM_TYPE_CODES

@login_required
@require_http_methods(["POST"])
def predict_fare_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid_input", "fields": {"body": "Invalid JSON"}}, status=400)

    distance_km = data.get('distance_km')
    weight_kg = data.get('weight_kg')
    item_type = data.get('item_type')

    fields_errors = {}
    
    if distance_km is None:
        fields_errors['distance_km'] = 'Required'
    else:
        try:
            distance_km = float(distance_km)
            if not (0.1 <= distance_km <= 10.0):
                fields_errors['distance_km'] = 'Must be between 0.1 and 10.0'
        except (ValueError, TypeError):
            fields_errors['distance_km'] = 'Must be a number'

    if weight_kg is None:
        fields_errors['weight_kg'] = 'Required'
    else:
        try:
            weight_kg = float(weight_kg)
            if not (0.1 <= weight_kg <= 20.0):
                fields_errors['weight_kg'] = 'Must be between 0.1 and 20.0'
        except (ValueError, TypeError):
            fields_errors['weight_kg'] = 'Must be a number'

    if item_type is None:
        fields_errors['item_type'] = 'Required'
    elif str(item_type).upper() not in ITEM_TYPE_CODES:
        fields_errors['item_type'] = 'Invalid item type'

    if fields_errors:
        return JsonResponse({"error": "invalid_input", "fields": fields_errors}, status=400)

    hour = datetime.now().hour

    try:
        fare = predict_fare(distance_km, weight_kg, hour, str(item_type).upper())
    except RuntimeError:
        return JsonResponse({"error": "model_not_trained"}, status=503)

    log(
        actor=request.user,
        action='FARE_PREDICTED',
        target_type='ML_Prediction',
        target_id=0,
        metadata={'fare': fare, 'distance_km': distance_km, 'item_type': item_type},
        ip=client_ip(request)
    )

    return JsonResponse({"fare": fare, "currency": "PKR"})

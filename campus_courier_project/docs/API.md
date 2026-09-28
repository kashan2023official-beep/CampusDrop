# API Endpoints

All endpoints are internal (AJAX) unless noted. CSRF token required for POST.

## `POST /api/predict-fare/`

**Request**
```json
{
  "distance_km": 1.8,
  "weight_kg": 2.5,
  "item_type": "DOCUMENT"
}
```

**Response 200**
```json
{ "fare": 132.5, "currency": "PKR" }
```

**Response 400**
```json
{ "error": "Invalid input", "fields": { "weight_kg": "Must be > 0" } }
```

## `GET /api/order/<id>/status/`

**Response 200**
```json
{
  "id": 42,
  "status": "ACCEPTED",
  "courier": "ali",
  "accepted_at": "2025-01-15T14:32:00Z"
}
```

Auth: sender or assigned courier only. Returns 403 otherwise.

## `GET /courier/available/json/`

**Response 200**
```json
[
  {
    "id": 42,
    "pickup_label": "Main Library",
    "dropoff_label": "Admin Block",
    "weight_kg": 2.5,
    "item_type": "DOCUMENT",
    "distance_km": 1.8,
    "predicted_fare": 132.5,
    "created_at": "2025-01-15T14:30:00Z"
  }
]
```

Auth: `courier_required`.

## `GET /api/campus-bounds/`

**Response 200**
```json
{
  "center": [31.5766, 74.3253],
  "bounds": [[31.5700, 74.3180], [31.5830, 74.3320]]
}
```

## Error Format (uniform)

```json
{ "error": "human-readable", "code": "MACHINE_CODE", "details": {} }
```

## HTTP Status Codes Used

| Code | Meaning |
|---|---|
| 200 | Success |
| 302 | Redirect (form POST) |
| 400 | Validation error |
| 403 | Not allowed (role/ownership) |
| 404 | Not found |
| 500 | Server error |

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
  "center": [31.579761694261773, 74.35494969618985],
  "bounds": [[31.5348, 74.3022], [31.6247, 74.4077]]
}
```

## `GET /api/landmarks/`

Returns all campus landmarks with coordinates and categories for map visualization.

**Response 200**
```json
{
  "landmarks": [
    {
      "name": "Main Library",
      "lat": 31.57811,
      "lon": 74.35502,
      "category": "academic"
    }
  ]
}
```
Auth: Authenticated users only. Returns 302/403 otherwise.

## `GET /api/reverse-geocode/?lat=<lat>&lon=<lon>`

Returns nearest landmark within 150m or falls back to coordinate string format.

**Response 200 (Landmark match)**
```json
{
  "label": "Computer Science Dept",
  "source": "landmark"
}
```

**Response 200 (Coordinate fallback)**
```json
{
  "label": "31.58250, 74.35250",
  "source": "coords"
}
```

**Response 400**
```json
{ "error": "invalid_params" }
// or
{ "error": "out_of_bounds" }
```
Auth: Authenticated users only.

## `GET /api/estimate-distance/?pickup_lat=...&pickup_lon=...&dropoff_lat=...&dropoff_lon=...`

Computes geodesic Haversine distance between two coordinates in kilometers.

**Response 200**
```json
{ "distance_km": 0.421 }
```
Auth: Authenticated users only.

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

# Database Schema

SQLite. All timestamps are `DateTimeField(auto_now_add=True)` unless noted.

## `auth.User` (Django built-in)

Standard Django user. Extended via `Profile`.

## `accounts.Profile`

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | AutoField | PK | |
| user | OneToOneField(User) | CASCADE | |
| is_courier | BooleanField | default=False | role toggle |
| phone | CharField(15) | blank=True | |
| rating | FloatField | default=5.0 | |
| created_at | DateTimeField | auto_now_add | |

## `orders.Order`

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | AutoField | PK | |
| sender | ForeignKey(User) | CASCADE, related_name='sent_orders' | |
| courier | ForeignKey(User) | SET_NULL, null=True, blank=True, related_name='courier_orders' | |
| pickup_lat | FloatField | | |
| pickup_lon | FloatField | | |
| pickup_label | CharField(120) | blank=True | |
| dropoff_lat | FloatField | | |
| dropoff_lon | FloatField | | |
| dropoff_label | CharField(120) | blank=True | |
| weight_kg | FloatField | validators=[MinValueValidator(0.1)] | |
| item_type | CharField(40) | choices | |
| notes | TextField | blank=True | |
| distance_km | FloatField | default=0.0 | haversine, computed on save |
| predicted_fare | FloatField | default=0.0 | from ML at creation |
| final_fare | FloatField | null=True, blank=True | set on delivery (later phase) |
| status | CharField(12) | choices, default='PENDING' | |
| created_at | DateTimeField | auto_now_add | |
| accepted_at | DateTimeField | null=True, blank=True | |
| picked_up_at | DateTimeField | null=True, blank=True | |
| delivered_at | DateTimeField | null=True, blank=True | |

### Item type choices
```
DOCUMENT, FOOD, ELECTRONICS, CLOTHING, BOOKS, OTHER
```

### Status choices
```
PENDING, ACCEPTED, PICKED_UP, DELIVERED, CANCELLED
```

### Indexes
- `status` (frequent filter in courier feed)
- `sender`, `courier`
- `created_at DESC`

## `core.AuditLog`

| Field | Type | Notes |
|---|---|---|
| id | AutoField | |
| actor | ForeignKey(User, null=True, SET_NULL) | who did it |
| action | CharField(40) | see below |
| target_type | CharField(40) | 'Order', 'User' |
| target_id | PositiveIntegerField | |
| metadata | JSONField | extra context |
| ip_address | GenericIPAddressField | null=True |
| created_at | DateTimeField | auto_now_add |

### Action values
```
ORDER_CREATED, ORDER_ACCEPTED, ORDER_PICKED_UP,
ORDER_DELIVERED, ORDER_CANCELLED,
ROLE_TOGGLED, USER_LOGIN, USER_LOGOUT,
FARE_PREDICTED
```

## Migrations Order

1. `accounts.0001_initial` (Profile)
2. `orders.0001_initial` (Order)
3. `core.0001_initial` (AuditLog)

# Audit Log

## Purpose
Append-only record of every state-changing action for demo, debugging, and academic reporting.

## Model
See `core.AuditLog` in DATABASE.md.

## Actions Logged

| Action | Trigger | Metadata |
|---|---|---|
| USER_LOGIN | successful login signal | `{}` |
| USER_LOGOUT | logout signal | `{}` |
| ROLE_TOGGLED | toggle-role view | `{"is_courier": true/false}` |
| ORDER_CREATED | order create view | `{"weight_kg": ..., "distance_km": ...}` |
| ORDER_ACCEPTED | accept view | `{"courier_id": ...}` |
| ORDER_PICKED_UP | pickup view | `{}` |
| ORDER_DELIVERED | deliver view | `{}` |
| ORDER_CANCELLED | cancel view | `{"reason": "user"}` |
| FARE_PREDICTED | predict view | `{"fare": 132.5, "distance_km": ...}` |

## Helper

```python
# core/audit.py
from .models import AuditLog

def log(actor, action, target_type, target_id, metadata=None, ip=None):
    AuditLog.objects.create(
        actor=actor if getattr(actor, 'is_authenticated', False) else None,
        action=action,
        target_type=target_type,
        target_id=target_id,
        metadata=metadata or {},
        ip_address=ip,
    )
```

## IP Extraction

```python
def client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0] if xff else request.META.get('REMOTE_ADDR')
```

## Viewing
- Insights panel: `/insights/audit/` (staff only) — paginated table, filter by action/actor.
- Django admin: `AuditLog` registered read-only (no add/change/delete).

## Retention
No deletion in v1. For long-running use, add a purge command later.

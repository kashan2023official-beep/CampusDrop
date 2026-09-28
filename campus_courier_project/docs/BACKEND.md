# Backend — Django

## Project Settings Highlights (`campus_courier/settings.py`)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'orders',
    'couriers',
    'ml_engine',
    'insights',
]

ALLOWED_HOSTS = ['*']
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

## App: `accounts`

### Models
- `Profile` (see DATABASE.md)

### Views (`accounts/views.py`)
| View | Method | URL | Purpose |
|---|---|---|---|
| `RegisterView` | GET/POST | `/register/` | signup, auto-create Profile |
| `LoginView` | GET/POST | `/login/` | Django auth |
| `LogoutView` | POST | `/logout/` | Django auth |
| `ProfileView` | GET/POST | `/profile/` | edit phone |
| `ToggleRoleView` | POST | `/toggle-role/` | flip `is_courier` |

### Decorators (`accounts/decorators.py`)

```python
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def courier_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not getattr(request.user, 'profile', None) or not request.user.profile.is_courier:
            messages.error(request, "Switch to courier mode first.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
```

### Signal
On `User` creation, auto-create `Profile`. Put in `accounts/signals.py`, wire in `accounts/apps.py`.

## App: `orders`

### Models
- `Order` (see DATABASE.md)

### Services (`orders/services.py`)

```python
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import AuditLog

ALLOWED = {
    'PENDING':   {'ACCEPTED', 'CANCELLED'},
    'ACCEPTED':  {'PICKED_UP', 'CANCELLED'},
    'PICKED_UP': {'DELIVERED'},
    'DELIVERED': set(),
    'CANCELLED': set(),
}

def transition(order, new_status, actor, ip=None):
    if new_status not in ALLOWED[order.status]:
        raise ValidationError(f"Cannot move {order.status} → {new_status}")
    order.status = new_status
    now = timezone.now()
    if new_status == 'ACCEPTED':
        order.courier = actor
        order.accepted_at = now
    elif new_status == 'PICKED_UP':
        order.picked_up_at = now
    elif new_status == 'DELIVERED':
        order.delivered_at = now
    order.save()
    AuditLog.objects.create(
        actor=actor, action=f"ORDER_{new_status}",
        target_type='Order', target_id=order.id,
        metadata={'new_status': new_status}, ip_address=ip,
    )
    return order
```

### Utils (`orders/utils.py`)
- `haversine(lat1, lon1, lat2, lon2) → km`
- `compute_distance(order) → float`

### Views
| View | Method | URL |
|---|---|---|
| `DashboardView` | GET | `/dashboard/` |
| `OrderCreateView` | GET/POST | `/orders/new/` |
| `OrderListView` | GET | `/orders/` |
| `OrderDetailView` | GET | `/orders/<id>/` |
| `OrderCancelView` | POST | `/orders/<id>/cancel/` |
| `PredictFareView` | POST | `/api/predict-fare/` |
| `OrderStatusJSON` | GET | `/api/order/<id>/status/` |
| `CampusBoundsView` | GET | `/api/campus-bounds/` |

## App: `couriers`

All views use `@login_required` + `@courier_required`.

| View | Method | URL |
|---|---|---|
| `AvailableOrdersView` | GET | `/courier/available/` |
| `AvailableOrdersJSON` | GET | `/courier/available/json/` |
| `AcceptOrderView` | POST | `/courier/accept/<id>/` |
| `PickupOrderView` | POST | `/courier/pickup/<id>/` |
| `DeliverOrderView` | POST | `/courier/deliver/<id>/` |
| `MyJobsView` | GET | `/courier/jobs/` |

Accept uses `select_for_update()` inside a transaction to prevent double-accept:

```python
from django.db import transaction

@transaction.atomic
def accept(request, pk):
    order = Order.objects.select_for_update().get(pk=pk, status='PENDING')
    transition(order, 'ACCEPTED', actor=request.user)
```

## App: `ml_engine`

- `predictor.py` — loads `fare_model.joblib`, exposes `predict_fare(distance_km, weight_kg, hour, item_type)`.
- `management/commands/train_fare_model.py` — generates synthetic data, trains, saves.
- `views.py::PredictFareView` — POST JSON, returns `{'fare': 145.0}`.

## App: `insights`

| View | URL | Purpose |
|---|---|---|
| `InsightsDashboard` | `/insights/` | KPI cards + Chart.js |
| `InsightsOrders` | `/insights/orders/` | table of all orders |
| `InsightsUsers` | `/insights/users/` | table of users + roles |

Access restricted to `is_staff=True`.

## App: `core`

- `models.py::AuditLog`
- `views.py::HomeView` — redirects logged-in users to `/dashboard/`, else `/login/`
- `context_processors.py::role_mode` — injects current mode into every template

## URL Root (`campus_courier/urls.py`)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('', include('orders.urls')),
    path('courier/', include('couriers.urls')),
    path('insights/', include('insights.urls')),
]
```

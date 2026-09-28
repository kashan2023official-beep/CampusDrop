# CAMPUS COURIER — MASTER BOOTSTRAP FILE

> **⚠️ READ THIS ENTIRE FILE BEFORE DOING ANYTHING.**
> This is the single source of truth for bootstrapping the Campus Courier project. It contains:
> 1. Instructions to you (the AI agent)
> 2. A complete list of every file you must create
> 3. The exact content of every file
>
> Do NOT deviate. Do NOT invent extra files. Do NOT skip any file.

---

## PART 0 — INSTRUCTIONS TO THE AI AGENT

### 0.1 Your Task

You are bootstrapping a Django project called **Campus Courier** for a university semester project. Your job in this session is **ONLY to create the following**:

1. The Django project scaffold (`campus_courier/`)
2. Empty Django apps: `core`, `accounts`, `orders`, `couriers`, `ml_engine`, `insights`
3. Every documentation file listed in PART 2 of this file, placed exactly where specified
4. `requirements.txt` and `.gitignore`

**DO NOT** implement Phase 1 view logic, models, migrations, or templates in this session. That happens in a later session. Your only job now is:
- Scaffold the project
- Create the empty apps
- Write all the documentation files verbatim
- Create `requirements.txt` and `.gitignore`

### 0.2 Rules

- Create files with **exact paths** given.
- Copy the content of each documentation file **verbatim**. Do not summarize, do not "improve", do not reformat.
- If a directory does not exist, create it.
- Use UTF-8 encoding. Use LF line endings.
- Do NOT install packages.
- Do NOT run migrations.
- Do NOT create superusers.
- Do NOT write any Python logic beyond what `django-admin startproject` and `startapp` produce.
- Do NOT add extra doc files, README sections, or comments beyond what is specified here.
- Do NOT wrap file content in extra code fences when writing files — write the raw content.

### 0.3 Execution Order

1. Create the folder `campus_courier_project/` (this will be the repo root).
2. Inside it, run `django-admin startproject campus_courier .` (project package at root, `manage.py` at root).
3. Inside it, run `python manage.py startapp core`, then `accounts`, `orders`, `couriers`, `ml_engine`, `insights`.
4. Create `docs/` directory at repo root.
5. Create the following files with the content given in PART 2:
   - `README.md`
   - `requirements.txt`
   - `.gitignore`
   - `docs/ARCHITECTURE.md`
   - `docs/TECH_STACK.md`
   - `docs/DATABASE.md`
   - `docs/BACKEND.md`
   - `docs/FRONTEND.md`
   - `docs/API.md`
   - `docs/ML.md`
   - `docs/SECURITY.md`
   - `docs/AUDIT_LOG.md`
   - `docs/PHASES.md`
   - `docs/DEPLOYMENT.md`
   - `docs/CONVENTIONS.md`
   - `docs/DECISIONS.md`
6. Confirm at the end by listing every path you created.

### 0.4 Final Directory Tree (expected result)

```
campus_courier_project/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── campus_courier/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── core/
├── accounts/
├── orders/
├── couriers/
├── ml_engine/
├── insights/
└── docs/
    ├── ARCHITECTURE.md
    ├── TECH_STACK.md
    ├── DATABASE.md
    ├── BACKEND.md
    ├── FRONTEND.md
    ├── API.md
    ├── ML.md
    ├── SECURITY.md
    ├── AUDIT_LOG.md
    ├── PHASES.md
    ├── DEPLOYMENT.md
    ├── CONVENTIONS.md
    └── DECISIONS.md
```

When you have created all the files above, respond with a plain list of paths (one per line). No commentary.

---

## PART 1 — PROJECT SUMMARY (context for you, do not write to any file)

**Campus Courier** is a hyperlocal parcel courier dispatch system for University of Engineering and Technology (UET), Lahore (Ghari Shahu campus). Senders create parcel orders. Couriers accept and deliver. Fare is ML-predicted in PKR. Mockup v1 is restricted to campus premises.

- Backend: Django 5.x
- DB: SQLite
- Frontend: Django templates + Tailwind CDN + vanilla JS + Leaflet
- Realtime: AJAX polling (5s)
- ML: scikit-learn Ridge regression
- Deploy: `runserver 0.0.0.0:8000` on LAN

The documentation files in PART 2 describe the full project. Some describe features not yet built (they describe the **target** state). That is intentional — they are the roadmap.

---

## PART 2 — FILE CONTENTS

Each subsection below specifies:
- **Path**: where to create the file
- **Content**: the exact content to write

Create each file with the exact path and exact content.

---

### FILE 1 — `README.md`

Path: `README.md`

Content:

```markdown
# Campus Courier — UET Lahore

A hyperlocal courier dispatch platform for University of Engineering and Technology, Lahore (Ghari Shahu campus). Senders create parcel orders, couriers accept and deliver them. Fare is predicted using a simple ML model. Currency: PKR.

## Status
Mockup v1 — restricted to campus premises. 5 km ring, billing, and bidding coming in later phases.

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py train_fare_model
python manage.py runserver 0.0.0.0:8000
```

Access from another device: `http://<host-ip>:8000`

## Documentation Index

| File | Purpose |
|---|---|
| `docs/ARCHITECTURE.md` | System design, apps, data flow |
| `docs/TECH_STACK.md` | Technologies and rationale |
| `docs/DATABASE.md` | Models, fields, relationships |
| `docs/BACKEND.md` | Django views, URLs, services |
| `docs/FRONTEND.md` | Templates, Tailwind, Leaflet, JS |
| `docs/API.md` | AJAX/REST endpoints |
| `docs/ML.md` | Fare prediction engine |
| `docs/SECURITY.md` | Auth, roles, decorators |
| `docs/AUDIT_LOG.md` | Audit logging spec |
| `docs/PHASES.md` | Build roadmap |
| `docs/DEPLOYMENT.md` | Local network setup |
| `docs/CONVENTIONS.md` | Coding standards |
| `docs/DECISIONS.md` | Architecture decision records |
```

---

### FILE 2 — `requirements.txt`

Path: `requirements.txt`

Content:

```
Django>=5.0,<5.1
scikit-learn>=1.4
joblib>=1.3
numpy>=1.26
pandas>=2.2
pytest>=8.0
pytest-django>=4.8
```

---

### FILE 3 — `.gitignore`

Path: `.gitignore`

Content:

```
venv/
env/
.venv/

__pycache__/
*.py[cod]
*$py.class

db.sqlite3
db.sqlite3-journal

*.joblib
*.log

.env
.env.*

.vscode/
.idea/
*.swp

.DS_Store
Thumbs.db

staticfiles/
media/
```

---

### FILE 4 — `docs/ARCHITECTURE.md`

Path: `docs/ARCHITECTURE.md`

Content:

```markdown
# Architecture

## Overview

Campus Courier is a monolithic Django application. Server-rendered HTML templates with Tailwind CSS, vanilla JavaScript for interactivity, and Leaflet for maps. AJAX polling (5s) provides pseudo-realtime updates. No WebSockets in v1.

## High-Level Diagram

```
┌─────────────────────────────────────────────────────┐
│                     Browser                         │
│  HTML + Tailwind (CDN) + Vanilla JS + Leaflet       │
└───────────────┬─────────────────────────────────────┘
                │ HTTP / AJAX (5s polling)
                ▼
┌─────────────────────────────────────────────────────┐
│              Django (runserver 0.0.0.0)             │
│                                                     │
│  accounts/   → auth, profile, role toggle           │
│  orders/     → create, list, detail, cancel         │
│  couriers/   → available, accept, pickup, deliver   │
│  ml_engine/  → train, predict fare                  │
│  insights/   → admin analytics panel                │
│  core/       → home, dashboard, base template       │
└───────────────┬─────────────────────────────────────┘
                │ ORM
                ▼
┌─────────────────────────────────────────────────────┐
│                     SQLite                          │
│  User, Profile, Order, AuditLog                     │
└─────────────────────────────────────────────────────┘
```

## Apps and Responsibilities

| App | Owns | Depends on |
|---|---|---|
| `core` | base template, dashboard, home | accounts |
| `accounts` | User, Profile, auth views, decorators | — |
| `orders` | Order model, sender views | accounts, ml_engine |
| `couriers` | Courier views, status transitions | orders, accounts |
| `ml_engine` | Training, model file, predict view | — |
| `insights` | Read-only analytics views | orders, accounts |

## Request Lifecycle (typical)

1. Browser hits `/orders/new/` (GET)
2. `OrderCreateView` renders `orders/create.html` with Leaflet map
3. User picks pickup/dropoff on map → hidden inputs filled
4. JS POSTs to `/api/predict-fare/` → returns fare
5. User submits form → `OrderCreateView` (POST) saves Order with `PENDING` status
6. `AuditLog` entry created
7. Redirect to `/orders/<id>/`

## Realtime Strategy

Couriers poll `/courier/available/json/` every 5 seconds. Response is a JSON list of pending orders. JS re-renders the list. Sender's order detail page polls `/api/order/<id>/status/` every 5 seconds to reflect courier actions.

## Status State Machine

```
PENDING ──► ACCEPTED ──► PICKED_UP ──► DELIVERED
   │            │
   └──► CANCELLED ◄──┘
```

Enforced in `orders/services.py::transition()`. Any illegal transition raises `ValidationError`.

## Folder Layout

```
campus_courier/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── campus_courier/          # project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
├── orders/
├── couriers/
├── ml_engine/
├── insights/
├── core/
├── templates/
├── static/
└── docs/
```
```

---

### FILE 5 — `docs/TECH_STACK.md`

Path: `docs/TECH_STACK.md`

Content:

```markdown
# Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Django 5 requirement |
| Framework | Django 5.x | Batteries-included, admin, ORM, auth |
| Database | SQLite | Zero-config, file-based, perfect for mockup |
| Frontend | Django templates | Server-rendered, simple |
| Styling | Tailwind CSS (CDN) | No build step, utility-first |
| Map | Leaflet.js + OpenStreetMap | Free, no API key |
| Interactivity | Vanilla JS | No React, no bundler |
| Charts | Chart.js (CDN) | Insights panel only |
| ML | scikit-learn + joblib | Linear/Ridge regression |
| Server | Django dev server | `0.0.0.0:8000`, local network |
| Testing | pytest-django, Django TestCase | Unit + view tests |

## Explicitly Not Used (v1)

- Docker
- React / Vue / Svelte
- WebSockets / Django Channels
- PostgreSQL / PostGIS
- Redis / Celery
- OTP / SMS
- Payment gateway
- npm / Vite / Webpack

## CDN Links (used in base.html)

```html
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

## Python Dependencies (`requirements.txt`)

```
Django>=5.0,<5.1
scikit-learn>=1.4
joblib>=1.3
numpy>=1.26
pandas>=2.2
pytest>=8.0
pytest-django>=4.8
```
```

---

### FILE 6 — `docs/DATABASE.md`

Path: `docs/DATABASE.md`

Content:

```markdown
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
```

---

### FILE 7 — `docs/BACKEND.md`

Path: `docs/BACKEND.md`

Content:

```markdown
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
```

---

### FILE 8 — `docs/FRONTEND.md`

Path: `docs/FRONTEND.md`

Content:

```markdown
# Frontend

Server-rendered Django templates + Tailwind CSS (CDN) + vanilla JS + Leaflet + Chart.js.

## Base Template (`templates/base.html`)

Structure:
```
<!doctype html>
<html>
<head>
  <title>{% block title %}Campus Courier{% endblock %}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  {% block head %}{% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
  <nav class="bg-white shadow"> ... </nav>
  <main class="max-w-5xl mx-auto px-4 py-6">
    {% for m in messages %}<div class="...">{{ m }}</div>{% endfor %}
    {% block content %}{% endblock %}
  </main>
  {% block scripts %}{% endblock %}
</body>
</html>
```

### Navbar
- Left: logo → `/dashboard/`
- Middle (if authenticated):
  - Sender mode links: My Orders, New Order
  - Courier mode links: Available, My Jobs
- Right:
  - Mode badge (Sender / Courier) + toggle button (POST form)
  - Profile, Logout

## Template Conventions

- Tailwind utility classes only. No custom CSS files unless unavoidable.
- Every form has `{% csrf_token %}`.
- Use `{% url 'name' %}` — never hardcode paths.
- Buttons that mutate state are always `<form method="post">`, never GET.
- Flash messages via Django messages framework.

## Key Templates

### `orders/create.html`
- Leaflet map (`#map`, `height: 400px`)
- Two hidden inputs: `pickup_lat`, `pickup_lon`, `dropoff_lat`, `dropoff_lon`
- Mode buttons: "Set Pickup", "Set Dropoff"
- Form fields: weight_kg, item_type, notes, pickup_label, dropoff_label
- Fare preview panel — calls `/api/predict-fare/` on change
- Map restricted to campus bounds

### `couriers/available.html`
- Polls `/courier/available/json/` every 5 s
- Renders list of cards
- Accept button per card → POST to `/courier/accept/<id>/`

### `orders/detail.html`
- Status timeline (PENDING → ACCEPTED → PICKED_UP → DELIVERED)
- Map with pickup + dropoff markers + polyline
- Courier info if assigned
- Sender sees "Cancel" if status is PENDING or ACCEPTED
- Polls `/api/order/<id>/status/` every 5 s to refresh status

## JavaScript Modules (`static/js/`)

### `map.js`
Exports `initOrderMap(boundsElId, pickupInputId, dropoffInputId)`.
```js
function initOrderMap(boundsUrl, opts) {
  const map = L.map('map', { maxBounds: opts.bounds, minZoom: 16 }).setView(opts.center, 17);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
  let mode = 'pickup';
  let pickupMarker, dropoffMarker;
  map.on('click', e => {
    if (mode === 'pickup') { /* set marker + inputs */ }
    else { /* set dropoff */ }
  });
  return { setMode: m => mode = m };
}
```

### `fare.js`
Debounced call to `/api/predict-fare/` on weight/type change. Updates `#fare-preview`.

### `polling.js`
Generic `pollEvery(url, ms, onData)` helper using `fetch`.

## Accessibility
- All form inputs have `<label>`.
- Buttons have descriptive text or `aria-label`.
- Focus states not removed from Tailwind defaults.

## Responsive
- Mobile-first. Navbar collapses on small screens.
- Map and forms stack vertically under `md:` breakpoint.
```

---

### FILE 9 — `docs/API.md`

Path: `docs/API.md`

Content:

```markdown
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
```

---

### FILE 10 — `docs/ML.md`

Path: `docs/ML.md`

Content:

```markdown
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
| hour | int | 0 – 23 |
| item_type_code | int | 0 – 5 (label-encoded) |

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

def predict_fare(distance_km, weight_kg, hour, item_type_code):
    X = [[distance_km, weight_kg, hour, item_type_code]]
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
```

---

### FILE 11 — `docs/SECURITY.md`

Path: `docs/SECURITY.md`

Content:

```markdown
# Security

## Authentication
- Django session-based auth.
- Passwords hashed with PBKDF2 (Django default).
- `LOGIN_URL = '/login/'` enforced via `@login_required`.

## Authorization Rules

| Resource | Rule |
|---|---|
| Order detail | sender OR assigned courier OR staff |
| Order cancel | sender only, and status ∈ {PENDING, ACCEPTED} |
| Accept order | any user with `is_courier=True` |
| Pickup / deliver | assigned courier only |
| Insights | `is_staff=True` only |
| Django admin | superuser only |

Enforced via custom decorators and object-level checks in views.

## CSRF
- All POST forms include `{% csrf_token %}`.
- AJAX POST sends `X-CSRFToken` header read from cookie.
- `CSRF_TRUSTED_ORIGINS` includes `http://<host-ip>:8000`.

## Session
- `SESSION_COOKIE_HTTPONLY = True` (default).
- `SESSION_COOKIE_SAMESITE = 'Lax'`.
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = False`.
- Session timeout: default 2 weeks (fine for demo).

## Input Validation
- Django forms for all user input.
- `MinValueValidator` on `weight_kg`.
- Lat/lon validated against campus bounds server-side on order creation.
- Item type restricted to `TextChoices`.

## Concurrency
- Order accept wrapped in `transaction.atomic()` + `select_for_update()` to prevent double-accept race.

## Audit
- Every state-changing action writes to `AuditLog` (see AUDIT_LOG.md).

## What We Are NOT Doing in v1
- HTTPS (local network only)
- Rate limiting
- 2FA
- OTP
- CAPTCHA
- Secrets management (dev-only `SECRET_KEY`)
```

---

### FILE 12 — `docs/AUDIT_LOG.md`

Path: `docs/AUDIT_LOG.md`

Content:

```markdown
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
```

---

### FILE 13 — `docs/PHASES.md`

Path: `docs/PHASES.md`

Content:

```markdown
# Build Phases

Each phase is independently runnable and testable. Do not start the next phase until the current one runs end-to-end.

---

## Phase 1 — Skeleton & Auth

**Deliverable:** Server runs, user can register/login/logout, role toggle works, navbar reflects mode.

**Tasks**
1. `django-admin startproject campus_courier .`
2. Create apps: `core accounts orders couriers ml_engine insights`
3. `settings.py`: add apps, `ALLOWED_HOSTS=['*']`, `LOGIN_URL`, templates dir, static dir
4. `Profile` model + signal to auto-create on User creation
5. `RegisterView`, use Django `LoginView`/`LogoutView`
6. `ProfileView` (edit phone), `ToggleRoleView`
7. `courier_required` decorator
8. `base.html` with Tailwind CDN + navbar
9. `home.html`, `dashboard.html`
10. Run migrations, create superuser, smoke-test

**Acceptance**
- Register → login → dashboard works
- Toggle role → navbar updates
- Logout works
- `python manage.py check` passes

---

## Phase 2 — Orders (No Map)

**Deliverable:** Sender can create an order with numeric lat/lon, list own orders, view detail, cancel.

**Tasks**
1. `Order` model + migration
2. `OrderCreateForm` (weight, item_type, pickup/dropoff lat/lon, labels, notes)
3. `haversine()` + auto-compute `distance_km` on save
4. Views: create, list, detail, cancel
5. `orders/services.py::transition()` with state machine
6. Templates: `create.html`, `list.html`, `detail.html`
7. Campus bounds validation server-side (hardcoded bbox)
8. Audit log entries on create/cancel

**Acceptance**
- Create order → appears in list → detail shows correct distance
- Cancel works only in PENDING/ACCEPTED
- Illegal transitions rejected

---

## Phase 3 — Courier Flow

**Deliverable:** Courier sees available orders, accepts, picks up, delivers. Sender sees status update.

**Tasks**
1. `AvailableOrdersView` + `AvailableOrdersJSON`
2. `available.html` with 5s polling + Accept buttons
3. `AcceptOrderView` with `transaction.atomic` + `select_for_update`
4. `PickupOrderView`, `DeliverOrderView`
5. `MyJobsView` for courier's accepted orders
6. `OrderStatusJSON` endpoint for sender polling
7. Sender detail page polls status
8. Audit log entries

**Acceptance**
- Two browsers: sender creates, courier accepts
- Double-accept prevented (test concurrency)
- Status flows PENDING → ACCEPTED → PICKED_UP → DELIVERED

---

## Phase 4 — Map

**Deliverable:** Leaflet map on order create. Click to set pickup/dropoff. Bounds restricted to campus. Polylines on detail page.

**Tasks**
1. `static/js/map.js` — reusable map initializer
2. `orders/create.html` embeds map + hidden inputs
3. `CampusBoundsView` returns center + bounds
4. Mode toggle buttons (pickup/dropoff)
5. Markers + labels
6. `orders/detail.html` static map with both markers + line
7. Client-side check: click outside bounds rejected
8. Server-side bounds validation on POST

**Acceptance**
- Map loads, clicks set coordinates
- Cannot place outside campus
- Detail page shows route line

---

## Phase 5 — ML Fare

**Deliverable:** Fare auto-predicted on order form. Model trained via command.

**Tasks**
1. `ml_engine/management/commands/train_fare_model.py`
2. Synthetic data generator + Ridge training + joblib dump
3. `ml_engine/predictor.py`
4. `PredictFareView` POST endpoint
5. `static/js/fare.js` — debounced AJAX
6. Fare preview on `create.html`
7. Save `predicted_fare` on order
8. Audit log `FARE_PREDICTED`

**Acceptance**
- `python manage.py train_fare_model` prints MAE
- Fare updates live on form
- Saved order has non-zero `predicted_fare`

---

## Phase 6 — Insights Panel

**Deliverable:** Staff-only analytics dashboard.

**Tasks**
1. `InsightsDashboard` with KPI cards (total orders, delivered, active couriers, avg delivery time)
2. Chart.js: orders per day (line), item type breakdown (pie), status breakdown (bar)
3. `InsightsOrders` table with filters
4. `InsightsUsers` table
5. `InsightsAudit` log table
6. Staff-only decorator

**Acceptance**
- `/insights/` loads with real data
- Non-staff gets 403

---

## Phase 7 — Polish & Demo

**Deliverable:** Demo-ready.

**Tasks**
1. Tailwind cleanup, responsive check
2. Empty states, loading spinners
3. Error pages (404, 500)
4. Basic tests (models, transitions, accept race, predict endpoint)
5. `README` quick start verified
6. Demo script written (`docs/DEMO.md`)
7. Seed data command for demo (`python manage.py seed_demo`)

**Acceptance**
- Two-browser demo works end to end
- `pytest` passes
- Someone else can clone + run following README
```

---

### FILE 14 — `docs/DEPLOYMENT.md`

Path: `docs/DEPLOYMENT.md`

Content:

```markdown
# Deployment — Local Network

## Host Machine Setup

1. Clone the repo.
2. Create virtualenv, install requirements.
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `python manage.py train_fare_model`
6. Run server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Finding Host IP

- Windows: `ipconfig` → look for IPv4 under active adapter
- Linux/Mac: `hostname -I` or `ifconfig`

## `settings.py` for LAN

```python
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://192.168.1.42:8000',   # replace with your host IP
]
```

## Client Devices

Open `http://<host-ip>:8000` in browser. Login with credentials created on host.

## Firewall

- Windows: allow Python through Windows Defender Firewall (private networks).
- Linux: `sudo ufw allow 8000/tcp`.

## Notes

- Django dev server is single-process. For 2–3 clients it's fine.
- If you need concurrency, run with `--noreload` and consider `gunicorn` later.
- Do NOT use in production. This is a LAN demo.

## Reset Database (demo)

```bash
del db.sqlite3          # Windows
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
```
```

---

### FILE 15 — `docs/CONVENTIONS.md`

Path: `docs/CONVENTIONS.md`

Content:

```markdown
# Coding Conventions

## Python

- PEP 8. Max line length 100.
- Type hints on all service functions and utils.
- Django CBVs preferred over FBVs where it saves lines.
- FBVs + decorators for simple action endpoints (accept, pickup, deliver).
- All business logic in `services.py`, not views.
- All input validation via Django Forms.

## Naming

- Models: `PascalCase`, singular (`Order`, not `Orders`)
- Views: `<Thing><Action>View` (`OrderCreateView`, `AcceptOrderView`)
- Templates: `snake_case`, mirror URL (`orders/create.html` for `/orders/new/`)
- URLs: kebab-case (`/predict-fare/`, `/toggle-role/`)
- Decorators: `<role>_required`

## Templates

- Indent 2 spaces.
- Blocks: `title`, `head`, `content`, `scripts`.
- No inline `<style>` unless unavoidable.
- Tailwind classes ordered: layout → spacing → typography → color → state.

## JavaScript

- Vanilla ES2020.
- One module per concern in `static/js/`.
- No global variables except the Leaflet map instance.
- `fetch` + async/await. No jQuery.

## Git

- Commit messages: `phase1: add profile model`, `phase3: fix accept race`
- One commit per logical change.
- `.gitignore`: `venv/`, `db.sqlite3`, `__pycache__/`, `*.joblib`, `.env`

## File Organization

- Group by app, not by type.
- Keep `views.py`, `models.py`, `forms.py`, `urls.py`, `services.py` in each app.
- Shared code goes in `core/`.

## Tests

- One test file per app: `tests.py` or `tests/` package.
- Test names: `test_<behavior>_<condition>`
- Use `pytest` markers: `@pytest.mark.django_db`

## Error Messages

- User-facing: friendly, no stack traces.
- Developer-facing: log with full context.
- API errors: `{ "error": str, "code": str, "details": dict }`
```

---

### FILE 16 — `docs/DECISIONS.md`

Path: `docs/DECISIONS.md`

Content:

```markdown
# Architecture Decision Records

Short ADR-style log. Each entry: decision, rationale, tradeoff.

---

### ADR-001: Monolithic Django, not microservices
**Decision:** Single Django project with multiple apps.  
**Why:** Team size, timeline, shared DB, one deploy target.  
**Tradeoff:** Harder to scale horizontally later. Acceptable for campus mockup.

---

### ADR-002: SQLite, not PostgreSQL
**Decision:** SQLite for v1.  
**Why:** Zero-config, file-based, easy to reset for demos.  
**Tradeoff:** Not concurrent-write friendly. Fine for <10 simultaneous users.

---

### ADR-003: Server-rendered templates, not React
**Decision:** Django templates + Tailwind CDN + vanilla JS.  
**Why:** Simplicity, no build step, faster iteration, team comfort.  
**Tradeoff:** Less interactive than a SPA. Acceptable given scope.

---

### ADR-004: Polling (5s), not WebSockets
**Decision:** AJAX polling for courier feed and order status.  
**Why:** Simpler, no Channels dependency, works on LAN.  
**Tradeoff:** Higher request volume. Acceptable for demo.

---

### ADR-005: Direct accept, not bidding
**Decision:** Courier accepts directly. No bidding for v1.  
**Why:** Reduces UI and backend complexity. Bidding can be added later.  
**Tradeoff:** Sender loses pricing leverage. Fare is ML-predicted instead.

---

### ADR-006: Ridge regression for fare
**Decision:** `sklearn.linear_model.Ridge` on 4 features.  
**Why:** Fast inference (<10ms), interpretable, easy to retrain.  
**Tradeoff:** Cannot learn non-linear patterns. Fine for synthetic data.

---

### ADR-007: Role toggle on Profile, not separate accounts
**Decision:** Single user account with `is_courier` boolean.  
**Why:** Sender can quickly become courier. Simpler than account linking.  
**Tradeoff:** One auth context for two roles. Manageable via decorators.

---

### ADR-008: No Docker
**Decision:** Run directly with `runserver`.  
**Why:** Simplicity, LAN-only target, no orchestration need.  
**Tradeoff:** Reproducibility relies on `requirements.txt` + README.

---

### ADR-009: AuditLog in `core`, not per-app
**Decision:** Single shared `AuditLog` model.  
**Why:** Uniform schema, single query surface for insights.  
**Tradeoff:** Generic fields (`target_type`, `target_id`) instead of FKs. Fine for demo.

---

### ADR-010: Tailwind via CDN, not build pipeline
**Decision:** `<script src="https://cdn.tailwindcss.com">`.  
**Why:** No npm, no build, works offline-ish with cached CDN.  
**Tradeoff:** Larger payload, no tree-shaking. Acceptable for demo.
```

---

## PART 3 — FINAL CHECKLIST FOR THE AI AGENT

Before responding, verify:

- [ ] `manage.py` exists at repo root
- [ ] `campus_courier/settings.py` exists
- [ ] All six apps created: `core`, `accounts`, `orders`, `couriers`, `ml_engine`, `insights`
- [ ] `docs/` contains exactly 13 `.md` files
- [ ] `README.md` at root
- [ ] `requirements.txt` at root
- [ ] `.gitignore` at root
- [ ] No extra files created
- [ ] No Python logic written beyond Django defaults

Respond with the plain list of every path created, one per line. Nothing else.

---

**END OF BOOTSTRAP FILE**
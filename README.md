# 📦 Campus Courier (CampusDrop) — UET Lahore

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.6-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Ridge%20Regression-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-199900.svg?logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Esri ArcGIS](https://img.shields.io/badge/Maps-Esri%20Satellite%20%2B%20Labels-007AC2.svg?logo=arcgis&logoColor=white)](https://www.esri.com/)
[![Tests](https://img.shields.io/badge/Tests-44%2F44%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

A modern, hyperlocal peer-to-peer parcel dispatch and courier platform engineered specifically for university campuses. Designed and calibrated for the **University of Engineering and Technology (UET), Lahore Main Campus**.

Campus Courier empowers students and faculty to seamlessly dispatch documents, food, books, electronics, and supplies across campus buildings, fulfilled by verified student couriers with machine-learning-driven dynamic fare estimation in Pakistani Rupees (PKR).

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [System Architecture & Tech Stack](#-system-architecture--tech-stack)
- [Campus Geofence & Coordinates](#-campus-geofence--coordinates)
- [Machine Learning Fare Predictor](#-machine-learning-fare-predictor)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Quick Start](#-installation--quick-start)
- [Pre-configured Demo Accounts](#-pre-configured-demo-accounts)
- [API Endpoints](#-api-endpoints)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Detailed Documentation Index](#-detailed-documentation-index)

---

## 🚀 Key Features

### 📍 Campus Landmarks & Map Visualization (Phase 11)
- **45+ Curated Campus Landmarks**: Comprehensive catalog covering academic blocks, faculties, student service centers, cafeterias, hostels, gates, and sports facilities.
- **Interactive Landmark Pins**: Visual `L.circleMarker` pins with instant hover tooltips and action popups to quickly "Set as Pickup" or "Set as Dropoff".
- **Intelligent Auto-Fill with Reverse Geocoding**: Proximity-based auto-fill (150m threshold) with debounced user-override preservation and coordinate fallback.
- **Dedicated Layer Switcher**: Integrated top-left toggle control to show or hide landmark pins on demand.

### 🧭 Courier Navigation Deep Links
- **One-Click Turn-by-Turn Routing**: Couriers on active delivery jobs can open Google Maps navigation deep links directly for both pickup and dropoff coordinates with zero API key dependencies.

### 🗺️ High-Resolution Esri Dual-Layer Mapping
- **Stacked Esri ArcGIS Imagery**: Powered by Esri `World_Imagery` (high-res satellite) stacked with `World_Boundaries_and_Places` (vector street labels and place names).
- **Interactive Layer Switcher**: Instant one-click toggle between **Satellite Mode** (for identifying campus departments, lawns, and hostels) and **Streets Mode** (for road navigation).
- **Point-and-Click Coordinate Selection**: Senders place interactive Pickup and Dropoff pins with automatic Haversine geodesic distance calculation and routing polylines.
- **Client & Server Geofence Enforcement**: Visual boundary polygons in Leaflet coupled with server-side validation rejecting coordinates outside university grounds.

### 🤖 Machine Learning Dynamic Fare Prediction
- **Ridge Regression Engine**: Predicts optimal delivery fares using distance, package weight, categorical item type, and campus rush hours.
- **Fair Pricing Model**: Calibrated with a base fee (50 PKR), per-kilometer rate (25 PKR/km), weight multiplier (10 PKR/kg), rush-hour surge (30 PKR), and category-specific handling bonuses.
- **Automatic Fallback Protection**: Heuristic fallback engine ensures zero downtime even before initial model training or in edge-case network conditions.

### 👥 Role-Based Workflows
- **Senders**: Create parcel delivery requests, input building pickup/dropoff points, select package categories, receive live ML fare estimates, track order statuses in real-time, and manage cancellations.
- **Couriers**: Browse available campus deliveries in the open order pool, claim deliveries with one click, and advance orders through verified lifecycles (`PENDING` ➔ `ACCEPTED` ➔ `PICKED_UP` ➔ `DELIVERED`).
- **Staff / Administrators**: Manage user permissions, promote couriers, inspect complete audit logs, and analyze platform performance.

### 🛡️ Enterprise-Grade Audit Logging & Security
- **Immutable Audit Trail**: All state changes, order acceptances, cancellations, and user role updates are permanently logged with timestamps, actor IDs, and client IP addresses.
- **Strict Access Control**: Enforced through custom decorators (`@courier_required`, `@staff_required`), CSRF verification, and database-level transaction integrity.

### 📊 Real-Time Analytics & Insights
- Executive dashboard tracking Gross Merchandise Volume (GMV), average delivery times, active courier capacity, order status distributions, and category trends.

---

## 🛠️ System Architecture & Tech Stack

| Component | Technology | Rationale |
|:---|:---|:---|
| **Backend Framework** | Django 5.0.6 (Python 3.11+) | Rapid development, built-in ORM, robust session authentication, and enterprise security. |
| **Machine Learning** | Scikit-Learn, NumPy, Joblib | Lightweight Ridge Regression for fast, deterministic, and interpretable fare predictions. |
| **Interactive Mapping** | Leaflet.js 1.9.4 | Fast, mobile-friendly interactive mapping without heavy commercial vendor SDKs. |
| **Map Tile Provider** | Esri ArcGIS Server | High-resolution satellite tiles (`World_Imagery`) and cartographic overlays with zero API keys required. |
| **Frontend Styling** | Tailwind CSS / Modern CSS3 | Clean, responsive card-based layout with glassmorphism accents and smooth micro-interactions. |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) | Zero-configuration local development transitioning to robust relational DB in production. |
| **Test Suite** | Pytest, Pytest-Django | Comprehensive test coverage for models, services, views, decorators, and ML predictions. |

---

## 📍 Campus Geofence & Coordinates

The platform restricts orders to the perimeter of **UET Lahore Main Campus**:

- **Campus Center**: `31.579762° N, 74.354950° E`
- **Geographic Bounding Box**:
  - **North**: `31.6247° N`
  - **South**: `31.5348° N`
  - **West**: `74.3022° E`
  - **East**: `74.4077° E`

Coordinates are dynamically served via `/api/campus-bounds/` to ensure single-source-of-truth alignment between Leaflet maps and Django form validators.

---

## 🧠 Machine Learning Fare Predictor

Fares are calculated in **Pakistani Rupees (PKR)** using an 8-dimensional feature representation:

$$\mathbf{X} = [\text{distance\_km}, \text{weight\_kg}, \text{is\_peak\_hour}, \text{food}, \text{electronics}, \text{clothing}, \text{books}, \text{other}]$$

### Feature Specs & Multipliers:
1. **Base Fare**: `50.00 PKR`
2. **Distance Multiplier**: `25.00 PKR / km`
3. **Weight Multiplier**: `10.00 PKR / kg`
4. **Campus Peak Surge**: `+30.00 PKR` during lecture rush hours (`08:00–10:00`, `12:00–14:00`, `17:00–19:00`)
5. **Item Category Bonuses**:
   - `DOCUMENT`: +0 PKR
   - `FOOD`: +15 PKR (spill risk & promptness)
   - `ELECTRONICS`: +40 PKR (high-value handling)
   - `CLOTHING`: +5 PKR
   - `BOOKS`: +5 PKR
   - `OTHER`: +10 PKR

The model is trained via `python manage.py train_fare_model` and serialized to `ml_engine/fare_model.joblib` with metadata in `ml_engine/fare_model.meta.json`.

---

## 📂 Project Directory Structure

```text
CampusDrop/
├── README.md                                # Root comprehensive documentation
├── main.md                                  # Workspace technical instructions
├── .gitignore                               # Global repository exclusions
└── campus_courier_project/
    ├── manage.py                            # Django management script
    ├── pytest.ini                           # Pytest test runner configuration
    ├── conftest.py                          # Pytest fixtures and DB setup
    ├── requirements.txt                     # Python dependencies
    ├── campus_courier/                      # Django project configuration
    │   ├── settings.py                      # Global application settings
    │   ├── urls.py                          # Root routing configuration
    │   └── wsgi.py                          # WSGI deployment entry point
    ├── accounts/                            # User authentication & courier profiles
    │   ├── models.py                        # Custom UserProfile & courier flags
    │   ├── views.py                         # Login, registration, profile views
    │   ├── decorators.py                    # @courier_required, @staff_required
    │   └── signals.py                       # Auto-create UserProfile post-save
    ├── orders/                              # Core parcel order lifecycle
    │   ├── models.py                        # Order entity & state transitions
    │   ├── forms.py                         # Geofenced order creation forms
    │   ├── landmarks.py                     # 45+ campus landmarks & haversine lookup
    │   ├── services.py                      # Order placement & cancellation logic
    │   ├── utils.py                         # Haversine calculation & campus bounds
    │   ├── views.py                         # Order creation, details, list views
    │   └── tests/                           # Order and landmark unit tests
    ├── couriers/                            # Courier dispatch workflow
    │   ├── views.py                         # Available jobs board, claim, deliver
    │   └── urls.py                          # Courier workflow endpoints
    ├── ml_engine/                           # Machine Learning fare estimator
    │   ├── predictor.py                     # Feature vectorizer & Ridge predictor
    │   ├── item_types.py                    # Categorical codes and bonus mappings
    │   ├── management/commands/
    │   │   └── train_fare_model.py          # Synthetic dataset generation & training
    │   └── views.py                         # POST /api/predict-fare/ endpoint
    ├── insights/                            # Administrative analytics dashboard
    │   ├── views.py                         # Volume, revenue, audit dashboards
    │   └── urls.py                          # Insights routing
    ├── core/                                # Audit logging & base layouts
    │   ├── models.py                        # AuditLog model
    │   ├── audit.py                         # log_action helper function
    │   └── management/commands/
    │       └── seed_demo.py                 # Comprehensive campus demo data seeder
    ├── static/                              # Static JavaScript & CSS assets
    │   ├── js/map.js                        # Interactive Leaflet map with Esri tiles
    │   └── js/static_map.js                 # Read-only order tracking map
    ├── templates/                           # Semantic HTML5 & Tailwind templates
    │   ├── base.html                        # Base application layout
    │   ├── accounts/                        # Auth & profile templates
    │   ├── orders/                          # Create order & detail views
    │   ├── couriers/                        # Available deliveries dashboard
    │   └── insights/                        # Admin metrics & audit views
    └── docs/                                # Detailed architectural specifications
        ├── ARCHITECTURE.md                  # System design & data flow
        ├── TECH_STACK.md                    # Technology stack rationale
        ├── DATABASE.md                      # Model schemas & ER relationships
        ├── BACKEND.md                       # Django views, services, urls
        ├── FRONTEND.md                      # UI/UX design & Leaflet integration
        ├── API.md                           # REST API endpoint contracts
        ├── ML.md                            # Mathematical fare model breakdown
        ├── SECURITY.md                      # Security, permissions, CSRF
        ├── AUDIT_LOG.md                     # Audit logging specifications
        ├── PHASES.md                        # Project milestone roadmap
        └── DEMO.md                          # Interactive evaluator walk-through
```

---

## ⚡ Installation & Quick Start

### 1. Prerequisites
- Python 3.11 or higher
- Git
- Virtual environment (`venv` or `conda`)

### 2. Clone the Repository
```bash
git clone https://github.com/kashan2023official-beep/CampusDrop.git
cd CampusDrop/campus_courier_project
```

### 3. Set Up Virtual Environment & Dependencies
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 4. Database Setup & Migrations
```bash
python manage.py migrate
```

### 5. Train the Machine Learning Fare Predictor
```bash
python manage.py train_fare_model
```
*Generates synthetic training records, fits Ridge regression, and creates `fare_model.joblib` and `fare_model.meta.json`.*

### 6. Populate Campus Demo Data
```bash
python manage.py seed_demo
```
*Seeds pre-configured senders, couriers, administrators, and 6 active/historical campus deliveries.*

### 7. Run the Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000/
```
*(Accessible across your local Wi-Fi network at `http://<your-ip>:8000/`)*

---

## 👤 Pre-configured Demo Accounts

All demo accounts share the password: **`DemoPass123!`**

| Username | Role | Description |
|:---|:---|:---|
| **`demo_sender`** | Sender | Student dispatching orders across UET departments. |
| **`demo_courier`** | Courier | Active student courier who can claim and complete deliveries. |
| **`demo_admin`** | Staff / Superuser | Full access to Django admin, Insights dashboard, and Audit logs. |

---

## 🔌 API Endpoints

### 1. Predict Fare
- **Endpoint**: `POST /api/predict-fare/`
- **Payload**:
  ```json
  {
    "pickup_lat": 31.5790,
    "pickup_lng": 74.3540,
    "dropoff_lat": 31.5810,
    "dropoff_lng": 74.3560,
    "weight_kg": 1.5,
    "item_type": "FOOD"
  }
  ```
- **Response**:
  ```json
  {
    "predicted_fare": 95.0,
    "distance_km": 0.298,
    "currency": "PKR",
    "fallback_used": false
  }
  ```

### 2. Campus Bounds
- **Endpoint**: `GET /api/campus-bounds/`
- **Response**:
  ```json
  {
    "center": [31.579761694261773, 74.35494969618985],
    "bounds": [[31.5348, 74.3022], [31.6247, 74.4077]]
  }
  ```

### 3. Campus Landmarks List
- **Endpoint**: `GET /api/landmarks/`
- **Response**:
  ```json
  {
    "landmarks": [
      { "name": "Main Library", "lat": 31.57811, "lon": 74.35502, "category": "academic" }
    ]
  }
  ```

### 4. Landmark Proximity & Reverse Geocoding
- **Endpoint**: `GET /api/reverse-geocode/?lat=31.5790&lon=74.3560`
- **Response**:
  ```json
  {
    "label": "Computer Science Dept",
    "source": "landmark"
  }
  ```

---

## 🧪 Testing & Quality Assurance

The platform features a comprehensive test suite written with `pytest-django`:

```bash
pytest -v
```

### Coverage Highlights:
- **Authentication & Contact Details**: Profile generation, Pakistani phone verification (`03xxxxxxxxx`), email uniqueness, courier promotions, role decorators.
- **Order Lifecycle & Contacts**: Order placements, status transitions, cancellation guards, conditional contact revelation (masked until ACCEPTED).
- **Landmark Geocoding & Visualization**: Landmark list expansion (45+ items), 150m threshold lookup, coordinate fallbacks, authenticated JSON API endpoint.
- **Courier Operations**: Available orders polling, race-condition handling with row-level locks, Google Maps navigation links, delivery confirmations.
- **Machine Learning Predictor**: Feature vector alignment, monotonicity verification, peak hour surge, fallback accuracy.
- **Insights & Audit**: Permissions gating for staff routes and audit log generation.

```text
accounts/tests/test_auth.py .......                         [  7% ]
accounts/tests/test_contact.py ..........                   [ 31% ]
couriers/tests/test_accept.py .......                       [ 41% ]
insights/tests/test_access.py .......                       [ 48% ]
ml_engine/tests/test_predictor.py .......                   [ 51% ]
orders/tests/test_landmarks.py .............                [ 63% ]
orders/tests/test_order.py ..........                       [ 78% ]
ml_engine/tests/test_predictor.py .......                   [ 85% ]
orders/tests/test_landmarks.py .............                [100% ]

============================= 44 passed in 29.84s =============================
```

---

## 📚 Detailed Documentation Index

For in-depth architecture and design documentation, consult the `docs/` folder:

| Document | Description |
|:---|:---|
| [`docs/ARCHITECTURE.md`](campus_courier_project/docs/ARCHITECTURE.md) | High-level system design, app boundaries, and data lifecycles. |
| [`docs/TECH_STACK.md`](campus_courier_project/docs/TECH_STACK.md) | Technical stack breakdown and architectural decision rationales. |
| [`docs/DATABASE.md`](campus_courier_project/docs/DATABASE.md) | Database entity relationships, schemas, and field constraints. |
| [`docs/BACKEND.md`](campus_courier_project/docs/BACKEND.md) | Django application structures, views, service layers, and routing. |
| [`docs/FRONTEND.md`](campus_courier_project/docs/FRONTEND.md) | UI/UX specifications, Tailwind components, and Leaflet map setup. |
| [`docs/API.md`](campus_courier_project/docs/API.md) | Complete REST API contract definitions and schemas. |
| [`docs/ML.md`](campus_courier_project/docs/ML.md) | Detailed ML model mathematical formulation and training pipeline. |
| [`docs/SECURITY.md`](campus_courier_project/docs/SECURITY.md) | Security protocols, role guards, CSRF handling, and sanitization. |
| [`docs/AUDIT_LOG.md`](campus_courier_project/docs/AUDIT_LOG.md) | Audit trail specification and event taxonomy. |
| [`docs/DEMO.md`](campus_courier_project/docs/DEMO.md) | Evaluator demo script and presentation checklist. |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details. Built with ❤️ for UET Lahore.

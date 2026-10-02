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

---

## Phase 8 — Contact Info & Conditional Reveal

**Deliverable:** Mandatory Pakistani phone number and unique email; contact info conditionally revealed only once order is ACCEPTED.

**Tasks**
1. Pakistani phone validation (`^03\d{9}$`) and unique email requirement on signup and profile editing
2. Mask contact details (`Hidden until accepted`) before an order is accepted
3. Unmask tel: and mailto: links server-side only when status is ACCEPTED, PICKED_UP, or DELIVERED
4. Staff-only insights users table with unmasked contact info

---

## Phase 9 — Landmark Auto-Fill & Google Navigation

**Deliverable:** Auto-fill location labels using nearest campus landmark on map click, and provide Google Maps navigation links.

**Tasks**
1. In-memory `CAMPUS_LANDMARKS` with initial locations and category taxonomy
2. Haversine proximity lookup (`find_nearest_landmark`, `describe_location`)
3. Reverse geocoding endpoint `/api/reverse-geocode/`
4. Free Google Maps navigation deep links on courier active jobs (`/courier/jobs/`)

---

## Phase 10 — Esri ArcGIS High-Res Mapping & Layer Switcher

**Deliverable:** Dual-layer satellite imagery with stacked street labels and instant mode toggle.

**Tasks**
1. Layer Esri `World_Imagery` with Esri `World_Boundaries_and_Places`
2. Esri `World_Street_Map` as street layer alternative
3. Top-right layer toggle control between Satellite and Streets modes

---

## Phase 11 — Landmark Visualization & UX Polish

**Deliverable:** Visual landmark pins on map, hover tooltips, click popups, layer toggle, and expanded landmarks list.

**Tasks**
1. Expand `CAMPUS_LANDMARKS` to 45+ locations across campus categories
2. Increase proximity auto-fill radius to 150m for more forgiving map clicks
3. `GET /api/landmarks/` endpoint returning all landmarks
4. Render `L.circleMarker` pins with hover tooltips and action popups ("Set as Pickup" / "Set as Dropoff")
5. Top-left "Landmarks" layer visibility toggle control
6. Fix userEdited flag with debouncing so manual edits don't permanently disable map auto-fill


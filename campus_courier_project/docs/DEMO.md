# Campus Courier — Evaluation & Demonstration Guide

This step-by-step walkthrough provides a complete, 10–15 step script to demonstrate the full lifecycle of the Campus Courier system to project evaluators and graders.

---

### Prerequisites & Seed Data

Ensure dependencies are installed, migrations applied, demo fixtures loaded, and fare model trained:

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py train_fare_model
```

Demo accounts available:
- **Sender User**: `demo_sender` / `DemoPass123!`
- **Courier User**: `demo_courier` / `DemoPass123!`
- **Staff / Admin User**: `demo_admin` / `DemoPass123!`

---

## Demonstration Script

### Step 1: Launch the Local Server
Start the development server listening on all interfaces:
```bash
python manage.py runserver 0.0.0.0:8000
```
Open your browser and navigate to `http://127.0.0.1:8000/`. Observe the automatic redirection to `/login/` for unauthenticated visitors.

### Step 2: Open Dual Browser Windows
Arrange two browser windows side by side:
- **Window A (Left)**: Chrome or Regular Window (Sender interface)
- **Window B (Right)**: Incognito / Firefox / Edge (Courier interface)

### Step 3: Authenticate Sender (Window A)
In Window A, log in with:
- **Username**: `demo_sender`
- **Password**: `DemoPass123!`

Observe the sender navigation bar: "My Orders", "New Order", role badge showing "Sender", and order history table with seeded orders.

### Step 4: Authenticate Courier (Window B)
In Window B, log in with:
- **Username**: `demo_courier`
- **Password**: `DemoPass123!`

Observe the courier navigation bar: "Available Orders", "My Jobs", and role badge showing "Courier".

### Step 5: Explore the Live Fare Estimator (Window A)
In Window A, click **New Order** (`/orders/new/`).
1. Click **Set Pickup** and click anywhere inside the UET Lahore campus boundary on the Leaflet map (e.g., near Main Gate).
2. Click **Set Dropoff** and click at another campus building (e.g., Computer Science Department).
3. Select an item type (e.g., **Electronics**).
4. Enter parcel weight (e.g., **2.5 kg**).
5. Watch the **Estimated Fare** panel: as inputs change, notice the subtle pulse animation while the backend ML model calculates and displays the predicted fare in real time (e.g., `≈ 220 PKR`).

### Step 6: Dispatch the New Parcel Order (Window A)
Add notes (e.g., *"Handle with care — circuit components"*) and click **Create Order**.
Observe the button showing a spinner with "Please wait..." and redirecting to the order detail page with status **PENDING**.

### Step 7: Real-Time Courier Discovery (Window B)
Switch to Window B and click **Available Orders** (`/courier/available/`).
The new order appears in the live polling list within 5 seconds without manual page refreshes.

### Step 8: Order Acceptance with Race-Condition Protection (Window B)
In Window B, click **Accept Order** on the newly created order.
- The order status atomically transitions to **ACCEPTED** via `select_for_update()`.
- The courier is redirected to **My Jobs**, displaying the active delivery with an embedded route preview map.

### Step 9: Automatic Status Synchronization (Window A)
Look back at Window A (Sender Detail view). Notice that the order timeline has automatically updated its status to **ACCEPTED** via client-side polling, showing the assigned courier `demo_courier`.

### Step 10: Package Pickup Transition (Window B)
In Window B on the **My Jobs** page, click **Mark Picked Up**.
- Status updates to **PICKED UP** on both the courier and sender views.
- Courier and pickup timestamp are recorded.

### Step 11: Final Delivery Confirmation (Window B)
In Window B, click **Mark Delivered**.
- The job moves from "Active Jobs" to "Job History".
- Sender window updates to **DELIVERED** with full completion timeline.

### Step 12: Inspect Administrative Insights Dashboard
In either window (or a new session), log in as the staff administrator:
- **Username**: `demo_admin`
- **Password**: `DemoPass123!`
Navigate to `/insights/`.
Examine:
- Aggregate KPI cards: Total Orders, Completed Deliveries, Pending Orders, and Registered Couriers.
- Comprehensive order table with statuses and fare distributions.

### Step 13: Verify Immutable Security Audit Trail
Scroll down to the **Recent Audit Logs** table on `/insights/` (or visit `/admin/core/auditlog/`).
Verify that each state-changing action throughout the lifecycle was logged:
- `ORDER_PENDING` / Order creation
- `FARE_PREDICTED` ML query
- `ORDER_ACCEPTED`
- `ORDER_PICKED_UP`
- `ORDER_DELIVERED`
Each record captures actor, action, timestamp, and client IP address.

### Step 14: Demonstration of Role Switching & Error Handling
- Show the **Switch to Courier / Switch to Sender** toggle button in the navbar.
- Navigate to an invalid URL such as `/nonexistent-route/` to showcase the custom branded **404 Page Not Found** template with direct return to the dashboard.

---

## Roadmap & Upcoming Features

Highlight planned extensions beyond the Phase 7 v1 campus prototype:
1. **5 km Extended Radius**: Expanding boundaries beyond campus gates to encompass student housing and markets in Garhi Shahu and Mughalpura.
2. **Integrated Billing & Wallet**: In-app digital payment integrations (Easypaisa / JazzCash) alongside cash on delivery.
3. **Courier Bidding System**: Allowing couriers to place competitive bids on high-priority or heavy parcel dispatches during peak hours.

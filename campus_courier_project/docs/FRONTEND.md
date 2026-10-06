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
- Map restricted to campus bounds with boundary box
- Interactive landmark pins (45+ `L.circleMarker`) fetched from `/api/landmarks/`
- Landmark hover tooltips and interactive popups with "Set as Pickup" and "Set as Dropoff" buttons
- "Landmarks" layer visibility checkbox control in top-left
- Auto-fill reverse geocoding from `/api/reverse-geocode/` with debounced user-edited protection
- Esri Satellite + Streets base layer switcher in top-right

### `couriers/available.html`
- Polls `/courier/available/json/` every 5 s
- Renders list of cards
- Accept button per card → POST to `/courier/accept/<id>/`

### `couriers/jobs.html`
- Renders courier's assigned active jobs and completed history
- Embedded static maps per job showing pickup and dropoff points
- Direct Google Maps navigation deep links (`https://www.google.com/maps/dir/?api=1&destination=<lat>,<lon>&travelmode=driving`) for turn-by-turn navigation to Pickup and Dropoff locations
- Action buttons for status progression (`Mark Picked Up`, `Mark Delivered`)

### `orders/detail.html`
- Status timeline (PENDING → ACCEPTED → PICKED_UP → DELIVERED)
- Map with pickup + dropoff markers + polyline
- Courier info if assigned (conditional contact reveal: phone & email revealed once ACCEPTED)
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

---

## Phase 13A: Design System Foundation

### Refined Color Tokens
- `brand.green`: `#22C55E` (primary CTA green)
- `brand.greenDark`: `#16A34A` (hover / pressed state)
- `brand.greenLight`: `#4ADE80` (accents)
- `brand.greenDarkText`: `#15803D` (text on soft green backgrounds)
- `brand.greenTint`: `#F0FDF4` (very soft background for icon circles)
- `brand.greenSoft`: `#DCFCE7` (soft chip and badge background)
- All CTA buttons with `bg-brand-green` use `text-white` for optimal contrast.

### UI Libraries
- **Alpine.js (v3 CDN)**: Loaded in `base.html` head with `[x-cloak]` display rule for lightweight reactive components and sheets.
- **Lucide Icons (CDN)**: Loaded via unpkg, automatically initialized with `lucide.createIcons()` and monitored via DOM MutationObserver.

### Reusable Template Components (`templates/components/`)
1. `_button.html`: Reusable button/link component supporting `primary`, `secondary`, `ghost`, `danger` variants, `sm`, `md`, `lg` sizes, Lucide icons (`icon`, `iconRight`), and full width.
2. `_card.html`: Clean container with `rounded-2xl`, `shadow-sm`, and optional `body_only` padding override.
3. `_badge.html`: Semantic badge chips supporting `green`, `yellow`, `blue`, `purple`, `red`, and `grey` colorways.
4. `_input.html`: Standardized text input field with optional label, leading Lucide icon, helper text, error text, and required flags.
5. `_sheet.html`: Alpine-driven mobile bottom sheet and desktop slide-over panel with backdrop, transition animations, and header controls.
6. `_empty_state.html`: Centered placeholder view featuring a green-tinted circular icon badge, title, descriptive text, and optional action button.


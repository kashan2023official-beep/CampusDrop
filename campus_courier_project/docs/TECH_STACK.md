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

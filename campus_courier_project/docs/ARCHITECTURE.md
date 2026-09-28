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

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

| File                   | Purpose                          |
| ---------------------- | -------------------------------- |
| `docs/ARCHITECTURE.md` | System design, apps, data flow   |
| `docs/TECH_STACK.md`   | Technologies and rationale       |
| `docs/DATABASE.md`     | Models, fields, relationships    |
| `docs/BACKEND.md`      | Django views, URLs, services     |
| `docs/FRONTEND.md`     | Templates, Tailwind, Leaflet, JS |
| `docs/API.md`          | AJAX/REST endpoints              |
| `docs/ML.md`           | Fare prediction engine           |
| `docs/SECURITY.md`     | Auth, roles, decorators          |
| `docs/AUDIT_LOG.md`    | Audit logging spec               |
| `docs/PHASES.md`       | Build roadmap                    |
| `docs/DEPLOYMENT.md`   | Local network setup              |
| `docs/CONVENTIONS.md`  | Coding standards                 |
| `docs/DECISIONS.md`    | Architecture decision records    |

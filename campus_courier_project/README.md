# 📦 Campus Courier Project — UET Lahore

A hyperlocal courier dispatch platform for University of Engineering and Technology, Lahore (Ghari Shahu campus). Senders create parcel orders, couriers accept and deliver them, with ML-predicted fares in PKR.

> 📖 **Full Documentation**: See the root [README.md](../README.md) for complete architectural diagrams, API contracts, ML formula derivations, and screenshots.

---

## ⚡ Quick Start

```bash
# 1. Activate your virtual environment
.\venv\Scripts\activate          # Windows
# source venv/bin/activate       # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Train the ML fare prediction model
python manage.py train_fare_model

# 5. Seed campus demo accounts and orders
python manage.py seed_demo

# 6. Start the development server
python manage.py runserver 0.0.0.0:8000
```

Access from any device on your local network: `http://<your-ip>:8000`

---

## 👤 Demo Accounts

Password for all seeded accounts: **`DemoPass123!`**

- **Sender**: `demo_sender`
- **Courier**: `demo_courier`
- **Administrator**: `demo_admin`

---

## 🧪 Running Tests

Run the complete 20-test automated test suite with `pytest`:

```bash
pytest -v
```

---

## 📚 Documentation Index

| File | Purpose |
|:---|:---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System design, app decomposition, data flow |
| [`docs/TECH_STACK.md`](docs/TECH_STACK.md) | Technologies and architectural rationale |
| [`docs/DATABASE.md`](docs/DATABASE.md) | Models, fields, foreign keys, relationships |
| [`docs/BACKEND.md`](docs/BACKEND.md) | Django views, URLs, services, decorators |
| [`docs/FRONTEND.md`](docs/FRONTEND.md) | Templates, CSS, Leaflet Esri satellite integration |
| [`docs/API.md`](docs/API.md) | AJAX/REST endpoints specification |
| [`docs/ML.md`](docs/ML.md) | Fare prediction Ridge regression engine & formula |
| [`docs/SECURITY.md`](docs/SECURITY.md) | Auth, roles, access decorators, CSRF |
| [`docs/AUDIT_LOG.md`](docs/AUDIT_LOG.md) | Transactional audit logging spec |
| [`docs/PHASES.md`](docs/PHASES.md) | Build roadmap and implementation phases |
| [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) | Local network & production setup |
| [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) | Code conventions & project standards |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Architecture decision records (ADRs) |
| [`docs/DEMO.md`](docs/DEMO.md) | Evaluator demo script & step-by-step guide |

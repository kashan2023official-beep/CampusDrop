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

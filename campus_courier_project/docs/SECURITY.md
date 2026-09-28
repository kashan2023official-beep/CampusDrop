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

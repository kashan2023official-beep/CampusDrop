# Coding Conventions

## Python

- PEP 8. Max line length 100.
- Type hints on all service functions and utils.
- Django CBVs preferred over FBVs where it saves lines.
- FBVs + decorators for simple action endpoints (accept, pickup, deliver).
- All business logic in `services.py`, not views.
- All input validation via Django Forms.

## Naming

- Models: `PascalCase`, singular (`Order`, not `Orders`)
- Views: `<Thing><Action>View` (`OrderCreateView`, `AcceptOrderView`)
- Templates: `snake_case`, mirror URL (`orders/create.html` for `/orders/new/`)
- URLs: kebab-case (`/predict-fare/`, `/toggle-role/`)
- Decorators: `<role>_required`

## Templates

- Indent 2 spaces.
- Blocks: `title`, `head`, `content`, `scripts`.
- No inline `<style>` unless unavoidable.
- Tailwind classes ordered: layout → spacing → typography → color → state.

## JavaScript

- Vanilla ES2020.
- One module per concern in `static/js/`.
- No global variables except the Leaflet map instance.
- `fetch` + async/await. No jQuery.

## Git

- Commit messages: `phase1: add profile model`, `phase3: fix accept race`
- One commit per logical change.
- `.gitignore`: `venv/`, `db.sqlite3`, `__pycache__/`, `*.joblib`, `.env`

## File Organization

- Group by app, not by type.
- Keep `views.py`, `models.py`, `forms.py`, `urls.py`, `services.py` in each app.
- Shared code goes in `core/`.

## Tests

- One test file per app: `tests.py` or `tests/` package.
- Test names: `test_<behavior>_<condition>`
- Use `pytest` markers: `@pytest.mark.django_db`

## Error Messages

- User-facing: friendly, no stack traces.
- Developer-facing: log with full context.
- API errors: `{ "error": str, "code": str, "details": dict }`

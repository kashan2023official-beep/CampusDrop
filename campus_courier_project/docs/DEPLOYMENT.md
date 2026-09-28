# Deployment — Local Network

## Host Machine Setup

1. Clone the repo.
2. Create virtualenv, install requirements.
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `python manage.py train_fare_model`
6. Run server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Finding Host IP

- Windows: `ipconfig` → look for IPv4 under active adapter
- Linux/Mac: `hostname -I` or `ifconfig`

## `settings.py` for LAN

```python
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://192.168.1.42:8000',   # replace with your host IP
]
```

## Client Devices

Open `http://<host-ip>:8000` in browser. Login with credentials created on host.

## Firewall

- Windows: allow Python through Windows Defender Firewall (private networks).
- Linux: `sudo ufw allow 8000/tcp`.

## Notes

- Django dev server is single-process. For 2–3 clients it's fine.
- If you need concurrency, run with `--noreload` and consider `gunicorn` later.
- Do NOT use in production. This is a LAN demo.

## Reset Database (demo)

```bash
del db.sqlite3          # Windows
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
```

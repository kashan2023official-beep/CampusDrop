import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_courier.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from orders.models import Order

# create two tight clusters
User.objects.filter(username='p15u').delete()
u = User.objects.create_user('p15u', password='StrongP@ss123!')
c = Client(); c.force_login(u)

# wipe any previous test orders
Order.objects.filter(sender=u).delete()

# cluster A around Main Library
for i in range(8):
    Order.objects.create(
        sender=u,
        pickup_lat=31.57811 + (i * 0.0001), pickup_lon=74.35502 + (i * 0.0001),
        pickup_label='Lib', dropoff_lat=31.58, dropoff_lon=74.356,
        dropoff_label='Adm', weight_kg=1.0, item_type='DOCUMENT',
        status='DELIVERED', distance_km=0.3, predicted_fare=120.0,
    )

# cluster B around Sports Cafeteria
for i in range(7):
    Order.objects.create(
        sender=u,
        pickup_lat=31.58060 + (i * 0.0001), pickup_lon=74.35580 + (i * 0.0001),
        pickup_label='Cafe', dropoff_lat=31.58, dropoff_lon=74.356,
        dropoff_label='Adm', weight_kg=1.0, item_type='FOOD',
        status='DELIVERED', distance_km=0.3, predicted_fare=150.0,
    )

from ml_engine.demand_hotspots import compute_hotspots, hotspots_available
assert hotspots_available()
hs = compute_hotspots()
print('Hotspots found:', len(hs))
for h in hs:
    print(f"  {h['label']:30s} count={h['count']} r={h['radius_km']:.3f} km at ({h['centroid_lat']:.5f}, {h['centroid_lon']:.5f})")
assert len(hs) >= 2, 'expected at least 2 clusters'

# endpoint
r = c.get('/api/hotspots/')
assert r.status_code == 200
body = r.json()
assert body['available'] is True
assert len(body['hotspots']) >= 2
print('hotspots endpoint OK')

# insights dashboard includes hotspots
admin = User.objects.filter(username='demo_admin').first()
if admin:
    ac = Client(); ac.force_login(admin)
    r = ac.get('/insights/')
    assert r.status_code == 200
    html = r.content.decode()
    assert 'Demand Hotspots' in html
    print('insights dashboard hotspots card OK')

Order.objects.filter(sender=u).delete()
u.delete()
print()
print('PHASE 15 VERIFIED SUCCESSFULLY!')

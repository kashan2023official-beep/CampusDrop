import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_courier.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from orders.models import Order

# find or create an ACCEPTED order
sender = User.objects.filter(username='demo_sender').first()
courier = User.objects.filter(username='demo_courier').first()
assert sender and courier

o = Order.objects.filter(status__in=['ACCEPTED','PICKED_UP','DELIVERED']).first()
if o is None:
    Order.objects.filter(sender=sender, pickup_label='chat-check').delete()
    o = Order.objects.create(
        sender=sender, courier=courier,
        pickup_lat=31.5797, pickup_lon=74.3549, pickup_label='chat-check',
        dropoff_lat=31.5800, dropoff_lon=74.3560, dropoff_label='Adm',
        weight_kg=1.0, item_type='DOCUMENT', status='ACCEPTED',
        distance_km=0.3, predicted_fare=120.0,
    )

sc = Client(); sc.force_login(sender)
r = sc.get(f'/orders/{o.id}/')
assert r.status_code == 200
html = r.content.decode()
assert 'open-chat' in html, 'chat trigger missing'
assert 'message-circle' in html, 'chat icon missing'
assert 'chat.js' in html, 'chat.js not loaded'
assert 'CURRENT_USER_ID' in html, 'user id not injected'
assert 'chatPanel' in html, 'chatPanel component missing'
print('sender sees chat trigger OK')

# courier side
cc = Client(); cc.force_login(courier)
r = cc.get(f'/orders/{o.id}/')
assert r.status_code == 200
html = r.content.decode()
assert 'open-chat' in html
assert 'chatPanel' in html
print('courier sees chat trigger OK')

# PENDING order should NOT have chat
o2 = Order.objects.filter(status='PENDING').first()
if o2:
    r = sc.get(f'/orders/{o2.id}/')
    html = r.content.decode()
    assert 'open-chat' not in html, 'chat should be hidden for PENDING'
    print('PENDING order has no chat OK')
else:
    print('no PENDING order to check (skip)')

# cleanup only if we created one
if o.pickup_label == 'chat-check':
    o.delete()

print()
print('PHASE 17B VERIFIED SUCCESSFULLY!')

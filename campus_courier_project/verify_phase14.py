import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_courier.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from orders.models import Order, Rating, CancelReason
from core.models import AuditLog

# clean prior test rows
User.objects.filter(username__in=['p14_sender','p14_courier']).delete()

sender = User.objects.create_user('p14_sender', password='StrongP@ss123!')
courier = User.objects.create_user('p14_courier', password='StrongP@ss123!')
courier.profile.is_courier = True
courier.profile.save()

sc = Client(); sc.force_login(sender)
cc = Client(); cc.force_login(courier)

# create + deliver an order
sc.post('/orders/new/', {
    'pickup_lat': 31.5797, 'pickup_lon': 74.3549, 'pickup_label': 'Lib',
    'dropoff_lat': 31.5800, 'dropoff_lon': 74.3560, 'dropoff_label': 'Adm',
    'weight_kg': 1.0, 'item_type': 'DOCUMENT', 'notes': ''
})
o = Order.objects.filter(sender=sender).latest('id')
cc.post(f'/courier/accept/{o.id}/')
cc.post(f'/courier/pickup/{o.id}/')
cc.post(f'/courier/deliver/{o.id}/')
o.refresh_from_db()
assert o.status == 'DELIVERED'
print('delivered order ready')

# --- rating happy path
r = sc.post(f'/orders/{o.id}/rate/', {'stars': '4', 'comment': 'Fast!'})
assert r.status_code == 302
assert Rating.objects.filter(order=o, rater=sender).exists()
courier.profile.refresh_from_db()
assert 4.0 <= courier.profile.rating <= 4.0
assert courier.profile.rating_count == 1
print('sender rating OK, courier rating =', courier.profile.rating)

# --- cannot rate twice
r = sc.get(f'/orders/{o.id}/')
assert o.can_be_rated_by(sender) == False
print('cannot rate twice OK')

# --- courier rates sender
r = cc.post(f'/orders/{o.id}/rate/', {'stars': '5', 'comment': 'Polite'})
assert r.status_code == 302
sender.profile.refresh_from_db()
assert sender.profile.rating == 5.0
assert sender.profile.rating_count == 1
print('courier rating OK')

# --- invalid stars rejected
sc.post('/orders/new/', {
    'pickup_lat': 31.5797, 'pickup_lon': 74.3549, 'pickup_label': 'L2',
    'dropoff_lat': 31.5800, 'dropoff_lon': 74.3560, 'dropoff_label': 'A2',
    'weight_kg': 1.0, 'item_type': 'DOCUMENT', 'notes': ''
})
o2 = Order.objects.filter(sender=sender, pickup_label='L2').latest('id')
cc.post(f'/courier/accept/{o2.id}/')
cc.post(f'/courier/pickup/{o2.id}/')
cc.post(f'/courier/deliver/{o2.id}/')
r = sc.post(f'/orders/{o2.id}/rate/', {'stars': '10'})
assert r.status_code == 302
assert not Rating.objects.filter(order=o2, rater=sender).exists()
print('invalid stars rejected OK')

# --- cancel reason required
sc.post('/orders/new/', {
    'pickup_lat': 31.5797, 'pickup_lon': 74.3549, 'pickup_label': 'L3',
    'dropoff_lat': 31.5800, 'dropoff_lon': 74.3560, 'dropoff_label': 'A3',
    'weight_kg': 1.0, 'item_type': 'DOCUMENT', 'notes': ''
})
o3 = Order.objects.filter(sender=sender, pickup_label='L3').latest('id')
r = sc.post(f'/orders/{o3.id}/cancel/', {})   # no reason
assert r.status_code == 302
o3.refresh_from_db()
assert o3.status == 'PENDING'
print('cancel without reason rejected OK')

r = sc.post(f'/orders/{o3.id}/cancel/', {
    'cancel_reason': 'CHANGE_OF_MIND', 'cancel_note': 'changed plans'
})
o3.refresh_from_db()
assert o3.status == 'CANCELLED'
assert o3.cancel_reason == 'CHANGE_OF_MIND'
assert o3.cancel_note == 'changed plans'
print('cancel with reason OK')

# --- audit log
assert AuditLog.objects.filter(action='ORDER_RATED').exists()
assert AuditLog.objects.filter(action='ORDER_CANCELLED').exists()
print('audit log entries OK')

# cleanup
Order.objects.filter(sender=sender).delete()
User.objects.filter(username__in=['p14_sender','p14_courier']).delete()
print()
print('PHASE 14 VERIFIED SUCCESSFULLY!')

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order
from ml_engine.demand_hotspots import compute_hotspots, hotspots_available

@pytest.mark.django_db
def test_compute_hotspots_returns_empty_when_no_data():
    Order.objects.all().delete()
    hotspots = compute_hotspots()
    assert hotspots == []

@pytest.mark.django_db
def test_compute_hotspots_finds_two_clear_clusters(sender_user, courier_user):
    # Cluster 1
    for i in range(8):
        Order.objects.create(
            sender=sender_user, courier=courier_user,
            pickup_lat=31.57811 + (i * 0.0001), pickup_lon=74.35502 + (i * 0.0001),
            pickup_label='Lib', dropoff_lat=31.58, dropoff_lon=74.356,
            weight_kg=1.0, item_type='DOCUMENT', status='DELIVERED', distance_km=0.3
        )
    # Cluster 2
    for i in range(7):
        Order.objects.create(
            sender=sender_user, courier=courier_user,
            pickup_lat=31.58060 + (i * 0.0001), pickup_lon=74.35580 + (i * 0.0001),
            pickup_label='Cafe', dropoff_lat=31.58, dropoff_lon=74.356,
            weight_kg=1.0, item_type='FOOD', status='DELIVERED', distance_km=0.3
        )

    assert hotspots_available()
    hotspots = compute_hotspots(min_samples=4, eps_km=0.15)
    assert len(hotspots) >= 2
    
    # Sort just to check the top two
    hotspots.sort(key=lambda x: x['count'], reverse=True)
    c1, c2 = hotspots[0], hotspots[1]
    
    assert c1['count'] >= 7
    assert c2['count'] >= 7

@pytest.mark.django_db
def test_hotspots_available_requires_minimum_orders(sender_user):
    Order.objects.all().delete()
    assert not hotspots_available()
    for _ in range(9):
        Order.objects.create(
            sender=sender_user, pickup_lat=31.5, pickup_lon=74.3, dropoff_lat=31.5, dropoff_lon=74.3,
            weight_kg=1.0, item_type='DOCUMENT', status='DELIVERED', distance_km=0.3
        )
    assert not hotspots_available()
    Order.objects.create(
        sender=sender_user, pickup_lat=31.5, pickup_lon=74.3, dropoff_lat=31.5, dropoff_lon=74.3,
        weight_kg=1.0, item_type='DOCUMENT', status='DELIVERED', distance_km=0.3
    )
    assert hotspots_available()

@pytest.mark.django_db
def test_hotspots_endpoint_requires_login(client):
    url = reverse('hotspots')
    r = client.get(url)
    assert r.status_code == 302
    assert r.url.startswith('/login/')

@pytest.mark.django_db
def test_hotspots_endpoint_returns_available_false_when_insufficient(client, sender_user):
    Order.objects.all().delete()
    client.force_login(sender_user)
    r = client.get(reverse('hotspots'))
    assert r.status_code == 200
    assert r.json()['available'] is False

@pytest.mark.django_db
def test_hotspots_endpoint_returns_clusters(client, sender_user, courier_user):
    client.force_login(sender_user)
    for _ in range(15):
        Order.objects.create(
            sender=sender_user, courier=courier_user,
            pickup_lat=31.578, pickup_lon=74.355, dropoff_lat=31.58, dropoff_lon=74.356,
            weight_kg=1.0, item_type='DOCUMENT', status='DELIVERED', distance_km=0.3
        )
    r = client.get(reverse('hotspots'))
    assert r.status_code == 200
    data = r.json()
    assert data['available'] is True
    assert len(data['hotspots']) >= 1

@pytest.mark.django_db
def test_insights_dashboard_includes_hotspots_context(client):
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
    client.force_login(admin)
    r = client.get(reverse('insights_dashboard'))
    assert r.status_code == 200
    assert 'hotspots' in r.context
    assert 'hotspots_available' in r.context

import pytest
from django.test import Client
from django.contrib.auth.models import User
from orders.models import Order, ItemType, Status
from orders.utils import compute_distance


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def sender_user(db):
    """Creates a regular sender user."""
    user = User.objects.create_user(
        username='test_sender',
        email='sender@test.local',
        password='TestPassword123!',
    )
    return user


@pytest.fixture
def courier_user(db):
    """Creates a courier user with profile.is_courier=True."""
    user = User.objects.create_user(
        username='test_courier',
        email='courier@test.local',
        password='TestPassword123!',
    )
    user.profile.is_courier = True
    user.profile.save()
    return user


@pytest.fixture
def staff_user(db):
    """Creates a staff user."""
    user = User.objects.create_user(
        username='test_staff',
        email='staff@test.local',
        password='TestPassword123!',
        is_staff=True,
    )
    return user


@pytest.fixture
def order_in_campus(db, sender_user):
    """Creates a PENDING order with coordinates inside campus bounds."""
    p_lat, p_lon = 31.5770, 74.3520
    d_lat, d_lon = 31.5800, 74.3580
    dist = compute_distance(p_lat, p_lon, d_lat, d_lon)
    order = Order.objects.create(
        sender=sender_user,
        pickup_lat=p_lat,
        pickup_lon=p_lon,
        pickup_label='Main Gate',
        dropoff_lat=d_lat,
        dropoff_lon=d_lon,
        dropoff_label='CS Department',
        weight_kg=1.0,
        item_type=ItemType.DOCUMENT,
        distance_km=dist,
        predicted_fare=150.0,
        status=Status.PENDING,
    )
    return order

import pytest
from django.core.exceptions import ValidationError
from orders.models import Order, Status, ItemType
from orders.services import transition
from orders.utils import compute_distance, is_inside_campus


@pytest.mark.django_db
def test_create_order_inside_bounds(client, sender_user):
    """Creating an order with coordinates inside campus bounds succeeds."""
    client.force_login(sender_user)
    payload = {
        'pickup_lat': 31.5770,
        'pickup_lon': 74.3520,
        'pickup_label': 'Main Gate',
        'dropoff_lat': 31.5800,
        'dropoff_lon': 74.3580,
        'dropoff_label': 'CS Department',
        'weight_kg': 1.5,
        'item_type': 'DOCUMENT',
        'notes': 'Deliver carefully',
    }
    response = client.post('/orders/new/', data=payload)
    assert response.status_code == 302

    order = Order.objects.filter(sender=sender_user).first()
    assert order is not None
    assert order.status == Status.PENDING
    assert order.pickup_label == 'Main Gate'
    assert order.dropoff_label == 'CS Department'


@pytest.mark.django_db
def test_create_order_outside_bounds_fails(client, sender_user):
    """Creating an order with coordinates outside campus bounds fails validation."""
    client.force_login(sender_user)
    payload = {
        'pickup_lat': 30.0000,  # Clearly outside campus bounds
        'pickup_lon': 70.0000,
        'pickup_label': 'Outside Pickup',
        'dropoff_lat': 31.5800,
        'dropoff_lon': 74.3580,
        'dropoff_label': 'CS Department',
        'weight_kg': 1.5,
        'item_type': 'DOCUMENT',
        'notes': 'Invalid location',
    }
    response = client.post('/orders/new/', data=payload)
    # Form redisplays with errors (HTTP 200) instead of redirecting
    assert response.status_code == 200
    assert Order.objects.filter(pickup_label='Outside Pickup').count() == 0


@pytest.mark.django_db
def test_distance_computed(order_in_campus):
    """Distance is automatically computed via haversine and greater than zero."""
    assert order_in_campus.distance_km > 0
    expected = compute_distance(
        order_in_campus.pickup_lat,
        order_in_campus.pickup_lon,
        order_in_campus.dropoff_lat,
        order_in_campus.dropoff_lon,
    )
    assert order_in_campus.distance_km == expected


@pytest.mark.django_db
def test_cancel_pending(client, sender_user, order_in_campus):
    """Sender can cancel a PENDING order."""
    client.force_login(sender_user)
    assert order_in_campus.status == Status.PENDING

    response = client.post(f'/orders/{order_in_campus.id}/cancel/', data={'cancel_reason': 'OTHER'})
    assert response.status_code == 302
    order_in_campus.refresh_from_db()
    assert order_in_campus.status == Status.CANCELLED


@pytest.mark.django_db
def test_cancel_delivered_fails(client, sender_user, order_in_campus):
    """Sender cannot cancel an order that has already been DELIVERED."""
    client.force_login(sender_user)
    order_in_campus.status = Status.DELIVERED
    order_in_campus.save()

    response = client.post(f'/orders/{order_in_campus.id}/cancel/')
    assert response.status_code == 302
    order_in_campus.refresh_from_db()
    assert order_in_campus.status == Status.DELIVERED


@pytest.mark.django_db
def test_illegal_transition_raises(sender_user, order_in_campus):
    """Attempting an invalid state transition raises ValidationError."""
    assert order_in_campus.status == Status.PENDING
    with pytest.raises(ValidationError):
        # Directly transitioning PENDING -> DELIVERED is illegal
        transition(order_in_campus, Status.DELIVERED, actor=sender_user)

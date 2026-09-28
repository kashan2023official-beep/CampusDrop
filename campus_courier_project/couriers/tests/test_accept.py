import pytest
from django.contrib.auth.models import User
from orders.models import Status
from orders.services import transition


@pytest.mark.django_db
def test_accept_pending(client, courier_user, order_in_campus):
    """Courier can successfully accept a PENDING order."""
    client.force_login(courier_user)
    assert order_in_campus.status == Status.PENDING

    response = client.post(f'/courier/accept/{order_in_campus.id}/')
    assert response.status_code == 302
    order_in_campus.refresh_from_db()
    assert order_in_campus.status == Status.ACCEPTED
    assert order_in_campus.courier == courier_user


@pytest.mark.django_db
def test_accept_already_taken_shows_error(client, courier_user, order_in_campus):
    """Attempting to accept an order that is already taken fails gracefully."""
    # First courier accepts it
    transition(order_in_campus, Status.ACCEPTED, actor=courier_user)

    # Create a second courier
    courier2 = User.objects.create_user(
        username='courier_two',
        email='c2@campus.local',
        password='TestPassword123!',
    )
    courier2.profile.is_courier = True
    courier2.profile.save()

    client.force_login(courier2)
    response = client.post(f'/courier/accept/{order_in_campus.id}/')
    assert response.status_code == 302
    order_in_campus.refresh_from_db()
    # Order remains assigned to courier_user
    assert order_in_campus.courier == courier_user
    assert order_in_campus.status == Status.ACCEPTED


@pytest.mark.django_db
def test_pickup_requires_assigned_courier(client, courier_user, order_in_campus):
    """Only the assigned courier can pick up the order; others receive 403."""
    transition(order_in_campus, Status.ACCEPTED, actor=courier_user)

    # Different courier attempts pickup
    intruder = User.objects.create_user(
        username='intruder_courier',
        email='intruder@campus.local',
        password='TestPassword123!',
    )
    intruder.profile.is_courier = True
    intruder.profile.save()

    client.force_login(intruder)
    response = client.post(f'/courier/pickup/{order_in_campus.id}/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_deliver_requires_assigned_courier(client, courier_user, order_in_campus):
    """Only the assigned courier can deliver the order; others receive 403."""
    transition(order_in_campus, Status.ACCEPTED, actor=courier_user)
    transition(order_in_campus, Status.PICKED_UP, actor=courier_user)

    intruder = User.objects.create_user(
        username='intruder_courier2',
        email='intruder2@campus.local',
        password='TestPassword123!',
    )
    intruder.profile.is_courier = True
    intruder.profile.save()

    client.force_login(intruder)
    response = client.post(f'/courier/deliver/{order_in_campus.id}/')
    assert response.status_code == 403

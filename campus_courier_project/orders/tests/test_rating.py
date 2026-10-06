import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order, Rating, CancelReason
from core.models import AuditLog


@pytest.mark.django_db
def test_rating_requires_delivered_status(client, sender_user, order_in_campus):
    client.force_login(sender_user)
    assert order_in_campus.status == 'PENDING'
    url = reverse('order_rate', args=[order_in_campus.id])
    resp = client.post(url, {'stars': 5, 'comment': ''})
    assert resp.status_code == 302
    assert not Rating.objects.filter(order=order_in_campus).exists()


@pytest.mark.django_db
def test_rating_requires_being_a_party(client, order_in_campus):
    third_user = User.objects.create_user(username='third', password='123')
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    client.force_login(third_user)
    url = reverse('order_rate', args=[order_in_campus.id])
    resp = client.post(url, {'stars': 5})
    assert resp.status_code == 302
    assert not Rating.objects.filter(order=order_in_campus).exists()


@pytest.mark.django_db
def test_rating_requires_login(client, order_in_campus):
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    url = reverse('order_rate', args=[order_in_campus.id])
    resp = client.post(url, {'stars': 5})
    assert resp.status_code == 302
    assert resp.url.startswith('/login/')
    assert not Rating.objects.filter(order=order_in_campus).exists()


@pytest.mark.django_db
def test_rating_rejects_invalid_stars(client, sender_user, courier_user, order_in_campus):
    order_in_campus.courier = courier_user
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    client.force_login(sender_user)
    url = reverse('order_rate', args=[order_in_campus.id])
    
    for invalid in [0, 6]:
        resp = client.post(url, {'stars': invalid})
        assert resp.status_code == 302
        assert not Rating.objects.filter(order=order_in_campus).exists()


@pytest.mark.django_db
def test_rating_saves_and_updates_profile(client, sender_user, courier_user, order_in_campus):
    order_in_campus.courier = courier_user
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    client.force_login(sender_user)
    url = reverse('order_rate', args=[order_in_campus.id])
    
    resp = client.post(url, {'stars': 4, 'comment': 'Good'})
    assert resp.status_code == 302
    assert Rating.objects.filter(order=order_in_campus, rater=sender_user).exists()
    
    courier_user.profile.refresh_from_db()
    assert courier_user.profile.rating == 4.0
    assert courier_user.profile.rating_count == 1


@pytest.mark.django_db
def test_rating_updates_on_second_rating(client, sender_user, courier_user, order_in_campus):
    # First rating by sender on order 1
    order_in_campus.courier = courier_user
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    client.force_login(sender_user)
    client.post(reverse('order_rate', args=[order_in_campus.id]), {'stars': 4})
    
    # Second order
    order2 = Order.objects.create(
        sender=sender_user, courier=courier_user, status='DELIVERED',
        pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1, item_type='FOOD'
    )
    # Second rating by sender on order 2
    client.post(reverse('order_rate', args=[order2.id]), {'stars': 2})
    
    courier_user.profile.refresh_from_db()
    assert courier_user.profile.rating == 3.0
    assert courier_user.profile.rating_count == 2


@pytest.mark.django_db
def test_cannot_rate_twice(client, sender_user, courier_user, order_in_campus):
    order_in_campus.courier = courier_user
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    client.force_login(sender_user)
    url = reverse('order_rate', args=[order_in_campus.id])
    
    client.post(url, {'stars': 5})
    assert not order_in_campus.can_be_rated_by(sender_user)
    
    resp = client.post(url, {'stars': 4}) # attempt again
    assert Rating.objects.filter(order=order_in_campus, rater=sender_user).count() == 1


@pytest.mark.django_db
def test_both_parties_can_rate(client, sender_user, courier_user, order_in_campus):
    order_in_campus.courier = courier_user
    order_in_campus.status = 'DELIVERED'
    order_in_campus.save()
    
    # Sender rates courier
    client.force_login(sender_user)
    client.post(reverse('order_rate', args=[order_in_campus.id]), {'stars': 4})
    
    # Courier rates sender
    client.force_login(courier_user)
    client.post(reverse('order_rate', args=[order_in_campus.id]), {'stars': 5})
    
    assert Rating.objects.filter(order=order_in_campus).count() == 2
    
    courier_user.profile.refresh_from_db()
    assert courier_user.profile.rating == 4.0
    sender_user.profile.refresh_from_db()
    assert sender_user.profile.rating == 5.0


@pytest.mark.django_db
def test_cancel_requires_reason(client, sender_user, order_in_campus):
    client.force_login(sender_user)
    url = reverse('order_cancel', args=[order_in_campus.id])
    resp = client.post(url, {}) # no reason
    assert resp.status_code == 302
    order_in_campus.refresh_from_db()
    assert order_in_campus.status == 'PENDING'


@pytest.mark.django_db
def test_cancel_saves_reason_and_note(client, sender_user, order_in_campus):
    client.force_login(sender_user)
    url = reverse('order_cancel', args=[order_in_campus.id])
    resp = client.post(url, {'cancel_reason': CancelReason.CHANGE_OF_MIND, 'cancel_note': 'Oops'})
    assert resp.status_code == 302
    order_in_campus.refresh_from_db()
    assert order_in_campus.status == 'CANCELLED'
    assert order_in_campus.cancel_reason == CancelReason.CHANGE_OF_MIND
    assert order_in_campus.cancel_note == 'Oops'


@pytest.mark.django_db
def test_cancel_reason_appears_in_audit_log(client, sender_user, order_in_campus):
    client.force_login(sender_user)
    url = reverse('order_cancel', args=[order_in_campus.id])
    client.post(url, {'cancel_reason': CancelReason.CHANGE_OF_MIND})
    
    log_entry = AuditLog.objects.filter(action='ORDER_CANCELLED', target_id=order_in_campus.id).first()
    assert log_entry is not None
    assert log_entry.metadata.get('cancel_reason') == CancelReason.CHANGE_OF_MIND


@pytest.mark.django_db
def test_cancel_reason_choices_are_all_valid(client, sender_user):
    client.force_login(sender_user)
    for choice in CancelReason.choices:
        reason = choice[0]
        # create a new order
        o = Order.objects.create(
            sender=sender_user, pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1, item_type='FOOD'
        )
        url = reverse('order_cancel', args=[o.id])
        resp = client.post(url, {'cancel_reason': reason})
        assert resp.status_code == 302
        o.refresh_from_db()
        assert o.status == 'CANCELLED'

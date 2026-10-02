import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order
from orders.services import transition

@pytest.mark.django_db
def test_signup_requires_email(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'phone': '03001234567',
        'password1': 'Pass123!',
        'password2': 'Pass123!',
    })
    assert response.status_code == 200
    assert 'email' in response.context['form'].errors

@pytest.mark.django_db
def test_signup_requires_phone(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@uet.edu.pk',
        'password1': 'Pass123!',
        'password2': 'Pass123!',
    })
    assert response.status_code == 200
    assert 'phone' in response.context['form'].errors

@pytest.mark.django_db
def test_signup_rejects_invalid_phone(client):
    for bad_phone in ["12345", "0412345678"]:
        response = client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@uet.edu.pk',
            'phone': bad_phone,
            'password1': 'Pass123!',
            'password2': 'Pass123!',
        })
        assert response.status_code == 200
        assert 'phone' in response.context['form'].errors

@pytest.mark.django_db
def test_signup_rejects_duplicate_email(client):
    User.objects.create_user(username='user1', email='test@uet.edu.pk', password='P1')
    response = client.post(reverse('register'), {
        'username': 'user2',
        'email': 'test@uet.edu.pk',
        'phone': '03001234567',
        'password1': 'Pass123!',
        'password2': 'Pass123!',
    })
    assert response.status_code == 200
    assert 'email' in response.context['form'].errors

@pytest.mark.django_db
def test_signup_success_creates_user_with_email_and_phone(client):
    response = client.post(reverse('register'), {
        'username': 'newuser',
        'email': 'new@uet.edu.pk',
        'phone': '03009999999',
        'password1': 'Pass123!',
        'password2': 'Pass123!',
    })
    assert response.status_code == 302
    user = User.objects.get(username='newuser')
    assert user.email == 'new@uet.edu.pk'
    assert user.profile.phone == '03009999999'

@pytest.mark.django_db
def test_profile_update_changes_email_and_phone(client):
    user = User.objects.create_user(username='testuser', email='old@uet.edu.pk', password='P1')
    user.profile.phone = '03000000000'
    user.profile.save()
    client.force_login(user)

    response = client.post(reverse('profile'), {
        'email': 'new@uet.edu.pk',
        'phone': '03001111111',
    })
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.email == 'new@uet.edu.pk'
    assert user.profile.phone == '03001111111'

@pytest.mark.django_db
def test_contact_hidden_before_accepted(client):
    sender = User.objects.create_user(username='sender', password='P')
    courier = User.objects.create_user(username='courier', password='P')
    courier.profile.phone = '03001234502'
    courier.profile.save()
    
    order = Order.objects.create(
        sender=sender, pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1
    )
    
    client.force_login(sender)
    response = client.get(reverse('order_detail', args=[order.id]))
    content = response.content.decode()
    assert 'No courier assigned yet' in content
    assert '03001234502' not in content

    # Edge case: courier assigned but status is PENDING
    order.courier = courier
    order.save()
    response = client.get(reverse('order_detail', args=[order.id]))
    content = response.content.decode()
    assert 'Hidden until accepted' in content
    assert '03001234502' not in content

@pytest.mark.django_db
def test_contact_visible_after_accepted(client):
    sender = User.objects.create_user(username='sender', password='P')
    courier = User.objects.create_user(username='courier', email='courier@uet.edu.pk', password='P')
    courier.profile.phone = '03001234502'
    courier.profile.is_courier = True
    courier.profile.save()
    
    order = Order.objects.create(
        sender=sender, pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1
    )
    client.force_login(courier)
    # Using services to transition properly
    transition(order, 'ACCEPTED', actor=courier, ip='127.0.0.1')
    
    client.force_login(sender)
    response = client.get(reverse('order_detail', args=[order.id]))
    content = response.content.decode()
    assert '03001234502' in content
    assert 'courier@uet.edu.pk' in content

@pytest.mark.django_db
def test_courier_sees_sender_contact_on_accepted_job(client):
    sender = User.objects.create_user(username='sender', email='sender@uet.edu.pk', password='P')
    sender.profile.phone = '03001234501'
    sender.profile.save()
    courier = User.objects.create_user(username='courier', password='P')
    courier.profile.is_courier = True
    courier.profile.save()
    
    order = Order.objects.create(
        sender=sender, pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1
    )
    transition(order, 'ACCEPTED', actor=courier, ip='127.0.0.1')
    
    client.force_login(courier)
    response = client.get(reverse('courier_jobs'))
    content = response.content.decode()
    assert '03001234501' in content
    assert 'sender@uet.edu.pk' in content

@pytest.mark.django_db
def test_available_json_never_exposes_sender_contact(client):
    sender = User.objects.create_user(username='sender', email='sender@uet.edu.pk', password='P')
    sender.profile.phone = '03001234501'
    sender.profile.save()
    courier = User.objects.create_user(username='courier', password='P')
    courier.profile.is_courier = True
    courier.profile.save()
    
    Order.objects.create(
        sender=sender, pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1
    )
    
    client.force_login(courier)
    response = client.get(reverse('courier_available_json'))
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert 'phone' not in item
        assert 'email' not in item
        assert '03001234501' not in str(item)
        assert 'sender@uet.edu.pk' not in str(item)

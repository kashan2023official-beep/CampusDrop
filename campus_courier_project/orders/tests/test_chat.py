import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from campus_courier.asgi import application
from orders.models import Order, ChatMessage

@database_sync_to_async
def create_test_order(sender, courier=None, status='PENDING'):
    return Order.objects.create(
        sender=sender, 
        courier=courier, 
        status=status,
        pickup_lat=0.0, pickup_lon=0.0,
        dropoff_lat=0.0, dropoff_lon=0.0,
        weight_kg=1.0, distance_km=1.0
    )

@database_sync_to_async
def create_user(username):
    return User.objects.create_user(username=username)

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_ws_requires_login():
    sender = await create_user('chat_sender_1')
    order = await create_test_order(sender, status='ACCEPTED')
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    communicator.scope['user'] = AnonymousUser()
    connected, subprotocol = await communicator.connect()
    
    assert not connected
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_ws_requires_party():
    sender = await create_user('chat_sender_2')
    third_party = await create_user('chat_third_2')
    order = await create_test_order(sender, status='ACCEPTED')
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    communicator.scope['user'] = third_party
    connected, subprotocol = await communicator.connect()
    
    assert not connected
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_ws_blocked_before_accept():
    sender = await create_user('chat_sender_3')
    order = await create_test_order(sender, status='PENDING')
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    communicator.scope['user'] = sender
    connected, subprotocol = await communicator.connect()
    
    assert not connected
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_ws_allows_after_accept():
    sender = await create_user('chat_sender_4')
    courier = await create_user('chat_courier_4')
    order = await create_test_order(sender, courier=courier, status='ACCEPTED')
    
    comm1 = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    comm1.scope['user'] = sender
    connected1, _ = await comm1.connect()
    assert connected1
    
    comm2 = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    comm2.scope['user'] = courier
    connected2, _ = await comm2.connect()
    assert connected2
    
    await comm1.disconnect()
    await comm2.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chat_ws_persists_and_broadcasts():
    sender = await create_user('chat_sender_5')
    courier = await create_user('chat_courier_5')
    order = await create_test_order(sender, courier=courier, status='ACCEPTED')
    
    comm_sender = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    comm_sender.scope['user'] = sender
    await comm_sender.connect()
    
    comm_courier = WebsocketCommunicator(application, f"/ws/order/{order.id}/chat/")
    comm_courier.scope['user'] = courier
    await comm_courier.connect()
    
    await comm_sender.send_json_to({'type': 'message', 'body': 'Hello WS'})
    
    # Both should receive the broadcast
    res_sender = await comm_sender.receive_json_from()
    res_courier = await comm_courier.receive_json_from()
    
    assert res_sender['type'] == 'message'
    assert res_sender['data']['body'] == 'Hello WS'
    assert res_sender['data']['sender_username'] == 'chat_sender_5'
    
    assert res_courier['type'] == 'message'
    assert res_courier['data']['body'] == 'Hello WS'
    
    # Verify DB persistence
    msg_count = await database_sync_to_async(ChatMessage.objects.filter(order=order).count)()
    assert msg_count == 1
    
    await comm_sender.disconnect()
    await comm_courier.disconnect()

@pytest.mark.django_db
def test_chat_history_endpoint_requires_party(client):
    sender = User.objects.create_user('chat_sender_6')
    third = User.objects.create_user('chat_third_6')
    order = Order.objects.create(sender=sender, status='ACCEPTED', pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1)
    
    client.force_login(third)
    response = client.get(reverse('order_messages_list', args=[order.id]))
    assert response.status_code == 403

@pytest.mark.django_db
def test_chat_history_endpoint_returns_messages_in_order(client):
    sender = User.objects.create_user('chat_sender_7')
    order = Order.objects.create(sender=sender, status='ACCEPTED', pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1)
    ChatMessage.objects.create(order=order, sender=sender, body='First')
    ChatMessage.objects.create(order=order, sender=sender, body='Second')
    
    client.force_login(sender)
    response = client.get(reverse('order_messages_list', args=[order.id]))
    assert response.status_code == 200
    data = response.json()
    assert data['chat_allowed'] is True
    assert len(data['messages']) == 2
    assert data['messages'][0]['body'] == 'First'
    assert data['messages'][1]['body'] == 'Second'

@pytest.mark.django_db
def test_chat_history_endpoint_blocked_before_accept(client):
    sender = User.objects.create_user('chat_sender_8')
    order = Order.objects.create(sender=sender, status='PENDING', pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1)
    
    client.force_login(sender)
    response = client.get(reverse('order_messages_list', args=[order.id]))
    assert response.status_code == 200
    data = response.json()
    assert data['chat_allowed'] is False
    assert data['messages'] == []

@pytest.mark.django_db
def test_chat_post_fallback_persists_message(client):
    sender = User.objects.create_user('chat_sender_9')
    order = Order.objects.create(sender=sender, status='ACCEPTED', pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1)
    
    client.force_login(sender)
    response = client.post(
        reverse('order_messages_create', args=[order.id]),
        data=json.dumps({'body': 'Fallback message'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json()['ok'] is True
    assert ChatMessage.objects.filter(order=order).count() == 1
    assert ChatMessage.objects.first().body == 'Fallback message'

@pytest.mark.django_db
def test_chat_post_fallback_rejects_empty_body(client):
    sender = User.objects.create_user('chat_sender_10')
    order = Order.objects.create(sender=sender, status='ACCEPTED', pickup_lat=0, pickup_lon=0, dropoff_lat=0, dropoff_lon=0, weight_kg=1)
    
    client.force_login(sender)
    response = client.post(
        reverse('order_messages_create', args=[order.id]),
        data=json.dumps({'body': '   '}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.json()['error'] == 'invalid_body'
    assert ChatMessage.objects.filter(order=order).count() == 0

import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser, User
from campus_courier.asgi import application
from orders.models import Order
from orders.services import transition
from channels.layers import get_channel_layer

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
def set_courier_profile(user):
    from accounts.models import Profile
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.is_courier = True
    profile.save()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_ws_order_requires_login():
    sender = await database_sync_to_async(User.objects.create_user)('ws_sender_1')
    order = await create_test_order(sender)
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/")
    communicator.scope['user'] = AnonymousUser()
    connected, subprotocol = await communicator.connect()
    
    assert not connected
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_ws_order_wrong_party():
    sender = await database_sync_to_async(User.objects.create_user)('ws_sender_2')
    other_courier = await database_sync_to_async(User.objects.create_user)('ws_other_courier_2')
    await set_courier_profile(other_courier)
    order = await create_test_order(sender)
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/")
    communicator.scope['user'] = other_courier
    connected, subprotocol = await communicator.connect()
    
    assert not connected
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_ws_order_initial_status():
    sender = await database_sync_to_async(User.objects.create_user)('ws_sender_3')
    order = await create_test_order(sender)
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/")
    communicator.scope['user'] = sender
    connected, subprotocol = await communicator.connect()
    assert connected
    
    response = await communicator.receive_json_from()
    assert response['type'] == 'status'
    assert response['data']['status'] == 'PENDING'
    
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_ws_order_broadcast_on_accept():
    sender = await database_sync_to_async(User.objects.create_user)('ws_sender_4')
    courier = await database_sync_to_async(User.objects.create_user)('ws_courier_4')
    await set_courier_profile(courier)
    order = await create_test_order(sender)
    
    communicator = WebsocketCommunicator(application, f"/ws/order/{order.id}/")
    communicator.scope['user'] = sender
    connected, subprotocol = await communicator.connect()
    assert connected
    
    await communicator.receive_json_from() # initial status
    
    await database_sync_to_async(transition)(order, 'ACCEPTED', courier)
    
    response = await communicator.receive_json_from()
    assert response['type'] == 'status'
    assert response['data']['status'] == 'ACCEPTED'
    
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_ws_courier_feed_requires_login():
    communicator = WebsocketCommunicator(application, "/ws/courier/available/")
    communicator.scope['user'] = AnonymousUser()
    connected, subprotocol = await communicator.connect()
    
    assert not connected
    await communicator.disconnect()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_ws_courier_feed_broadcast():
    courier = await database_sync_to_async(User.objects.create_user)('ws_courier_5')
    await set_courier_profile(courier)
    courier = await database_sync_to_async(User.objects.get)(username='ws_courier_5')
    
    communicator = WebsocketCommunicator(application, "/ws/courier/available/")
    communicator.scope['user'] = courier
    connected, subprotocol = await communicator.connect()
    assert connected
    
    layer = get_channel_layer()
    await layer.group_send(
        'couriers',
        {'type': 'order_available', 'data': {'id': 999}}
    )
    
    response = await communicator.receive_json_from()
    assert response['type'] == 'order_available'
    assert response['data']['id'] == 999
    
    await communicator.disconnect()

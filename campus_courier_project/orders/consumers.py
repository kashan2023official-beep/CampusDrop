from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Order

@sync_to_async
def check_order_access(order_id, user):
    try:
        order = Order.objects.get(id=order_id)
        return user.id in (order.sender_id, order.courier_id)
    except Order.DoesNotExist:
        return False

@sync_to_async
def get_order_data(order_id):
    try:
        order = Order.objects.select_related('courier', 'sender').get(id=order_id)
        return {
            'id': order.id,
            'status': order.status,
            'courier': order.courier.username if order.courier else None,
            'pickup_label': order.pickup_label,
            'dropoff_label': order.dropoff_label,
        }
    except Order.DoesNotExist:
        return {}

@sync_to_async
def check_courier_access(user):
    return hasattr(user, 'profile') and user.profile.is_courier


class OrderStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.order_id = self.scope['url_route']['kwargs']['order_id']
        
        has_access = await check_order_access(self.order_id, user)
        if not has_access:
            await self.close(code=1008)
            return

        self.group_name = f'order_{self.order_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        order_data = await get_order_data(self.order_id)
        await self.send_json({
            'type': 'status',
            'data': order_data,
        })

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        pass

    async def order_status_changed(self, event):
        order_id = event.get('order_id', self.order_id)
        order_data = await get_order_data(order_id)
        await self.send_json({
            'type': 'status',
            'data': order_data,
        })


class CourierFeedConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        is_courier = await check_courier_access(user)
        if not is_courier:
            await self.close(code=1008)
            return

        self.group_name = 'couriers'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        pass

    async def order_available(self, event):
        await self.send_json(event)

    async def order_taken(self, event):
        await self.send_json(event)


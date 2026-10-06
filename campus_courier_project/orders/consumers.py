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


class OrderChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if user is None or not user.is_authenticated:
            await self.close()
            return

        self.order_id = self.scope['url_route']['kwargs']['order_id']
        order = await sync_to_async(self._fetch_order)()
        if order is None:
            await self.close()
            return

        if not (order['is_party'] or user.is_staff):
            await self.close(code=4003)
            return

        if not order['chat_allowed']:
            await self.close(code=4004)
            return

        self.group_name = f'order_{self.order_id}_chat'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    def _fetch_order(self):
        from orders.models import Order
        o = Order.objects.filter(pk=self.order_id).first()
        if o is None:
            return None
        user = self.scope.get('user')
        return {
            'is_party': (o.sender_id == user.id or o.courier_id == user.id),
            'chat_allowed': o.chat_allowed(),
        }

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get('type') == 'ping':
            await self.send_json({'type': 'pong'})
            return

        if content.get('type') != 'message':
            return

        body = (content.get('body') or '').strip()
        if not body or len(body) > 2000:
            await self.send_json({'type': 'error', 'error': 'invalid_body'})
            return

        msg = await sync_to_async(self._save_message)(body)
        if msg is None:
            await self.send_json({'type': 'error', 'error': 'save_failed'})
            return

        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'chat_message', 'data': msg},
        )

    def _save_message(self, body):
        from orders.models import ChatMessage
        user = self.scope.get('user')
        try:
            m = ChatMessage.objects.create(
                order_id=self.order_id, sender=user, body=body)
            return {
                'id': m.id,
                'sender_id': m.sender_id,
                'sender_username': m.sender.username,
                'body': m.body,
                'created_at': m.created_at.isoformat(),
            }
        except Exception:
            return None

    async def chat_message(self, event):
        await self.send_json({'type': 'message', 'data': event['data']})

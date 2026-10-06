from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/order/(?P<order_id>\d+)/$',
            consumers.OrderStatusConsumer.as_asgi()),
    re_path(r'^ws/order/(?P<order_id>\d+)/chat/$',
            consumers.OrderChatConsumer.as_asgi()),
    re_path(r'^ws/courier/available/$',
            consumers.CourierFeedConsumer.as_asgi()),
]

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_courier.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from orders.models import Order

o = Order.objects.get(id=51)
print(f'order 51: status={o.status}  chat_allowed={o.chat_allowed()}')

u = User.objects.get(username='demo_sender')
c = Client(); c.force_login(u)
r = c.get(f'/orders/{o.id}/')
html = r.content.decode()

checks = {
  'open-chat button': 'open-chat' in html,
  'chatPanel component': 'chatPanel' in html,
  'message-circle icon': 'message-circle' in html,
  'CURRENT_USER_ID script': 'CURRENT_USER_ID' in html,
  'chat.js loaded': 'js/chat.js' in html,
  'Tailwind CDN removed': 'cdn.tailwindcss.com' not in html,
  'compiled CSS linked': 'css/tailwind.css' in html,
}
for k, v in checks.items():
    print(f'{k}: {v}')

import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.decorators import staff_required
from orders.models import Order, ItemType
from core.models import AuditLog
from ml_engine.demand_hotspots import compute_hotspots, hotspots_available


@login_required
@staff_required
def insights_dashboard(request):
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status='DELIVERED').count()
    pending_orders = Order.objects.filter(status='PENDING').count()
    active_couriers = User.objects.filter(profile__is_courier=True).count()
    total_users = User.objects.count()

    recent_orders = Order.objects.select_related('sender', 'courier').order_by('-created_at')[:10]
    recent_audits = AuditLog.objects.select_related('actor').order_by('-created_at')[:10]

    # 1. Orders per day (last 14 days, zero-filled)
    today = timezone.localdate()
    start_date = today - timedelta(days=13)
    daily_qs = (
        Order.objects.filter(created_at__date__gte=start_date)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    counts_by_day = {item['day']: item['count'] for item in daily_qs}
    orders_per_day = [
        {
            'date': (start_date + timedelta(days=i)).strftime('%b %d'),
            'count': counts_by_day.get(start_date + timedelta(days=i), 0)
        }
        for i in range(14)
    ]
    chart_orders_json = json.dumps(orders_per_day)

    # 2. Deliveries by Item Type
    item_counts = (
        Order.objects.values('item_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    item_choices = dict(ItemType.choices)
    item_type_data = [
        {
            'item_type': item['item_type'],
            'label': item_choices.get(item['item_type'], item['item_type'].title()),
            'count': item['count']
        }
        for item in item_counts
    ]
    chart_item_json = json.dumps(item_type_data)

    # 3. Deliveries by Courier (Top 5)
    courier_counts = (
        Order.objects.filter(status='DELIVERED', courier__isnull=False)
        .values('courier__username')
        .annotate(count=Count('id'))
        .filter(count__gt=0)
        .order_by('-count')[:5]
    )
    courier_data = [
        {
            'username': c['courier__username'],
            'count': c['count']
        }
        for c in courier_counts
    ]
    chart_courier_json = json.dumps(courier_data)

    context = {
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'active_couriers': active_couriers,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'recent_audits': recent_audits,
        'hotspots': compute_hotspots() if hotspots_available() else [],
        'hotspots_available': hotspots_available(),
        'chart_orders_json': chart_orders_json,
        'chart_item_json': chart_item_json,
        'chart_courier_json': chart_courier_json,
    }
    return render(request, 'insights/dashboard.html', context)


@login_required
@staff_required
def insights_orders(request):
    status_filter = request.GET.get('status')
    qs = Order.objects.select_related('sender', 'courier').order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'insights/orders.html', {'orders': qs, 'current_filter': status_filter})


@login_required
@staff_required
def insights_users(request):
    users = (
        User.objects.select_related('profile')
        .annotate(
            delivery_count=Count(
                'courier_orders',
                filter=Q(courier_orders__status='DELIVERED')
            )
        )
        .defer('password')
        .order_by('-delivery_count', '-date_joined')
    )
    return render(request, 'insights/users.html', {'users': users})


@login_required
@staff_required
def insights_audit(request):
    audits = AuditLog.objects.select_related('actor').order_by('-created_at')[:100]
    return render(request, 'insights/audit.html', {'audits': audits})


# Aliases for flexibility
insights_dashboard_view = insights_dashboard
insights_orders_view = insights_orders
insights_users_view = insights_users
insights_audit_view = insights_audit

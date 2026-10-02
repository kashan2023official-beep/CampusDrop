from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.decorators import staff_required
from orders.models import Order
from core.models import AuditLog


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

    context = {
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'active_couriers': active_couriers,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'recent_audits': recent_audits,
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
    users = User.objects.select_related('profile').defer('password').order_by('-date_joined')
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

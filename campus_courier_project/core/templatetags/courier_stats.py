from django import template
from orders.models import Order

register = template.Library()


@register.simple_tag
def courier_stats(user):
    """
    Returns courier statistics, the most recent active job, and up to 3 available pending orders.
    """
    if not user or not user.is_authenticated:
        return {
            'available_count': 0,
            'active_count': 0,
            'delivered_count': 0,
            'active_job': None,
            'available_orders': [],
        }

    available_qs = Order.objects.filter(status='PENDING').exclude(sender=user).order_by('-created_at')
    active_qs = Order.objects.filter(courier=user, status__in=['ACCEPTED', 'PICKED_UP']).order_by('-created_at')
    delivered_count = Order.objects.filter(courier=user, status='DELIVERED').count()

    return {
        'available_count': available_qs.count(),
        'active_count': active_qs.count(),
        'delivered_count': delivered_count,
        'active_job': active_qs.first(),
        'available_orders': list(available_qs[:3]),
    }

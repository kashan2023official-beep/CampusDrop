from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import AuditLog

ALLOWED = {
    'PENDING': {'ACCEPTED', 'CANCELLED'},
    'ACCEPTED': {'PICKED_UP', 'CANCELLED'},
    'PICKED_UP': {'DELIVERED'},
    'DELIVERED': set(),
    'CANCELLED': set(),
}


def transition(order, new_status, actor, ip=None):
    if new_status not in ALLOWED.get(order.status, set()):
        raise ValidationError(f"Cannot move {order.status} → {new_status}")

    order.status = new_status
    now = timezone.now()

    if new_status == 'ACCEPTED':
        order.courier = actor
        order.accepted_at = now
    elif new_status == 'PICKED_UP':
        order.picked_up_at = now
    elif new_status == 'DELIVERED':
        order.delivered_at = now

    order.save()

    AuditLog.objects.create(
        actor=actor if getattr(actor, 'is_authenticated', False) else None,
        action=f"ORDER_{new_status}",
        target_type='Order',
        target_id=order.id,
        metadata={'new_status': new_status},
        ip_address=ip,
    )
    return order

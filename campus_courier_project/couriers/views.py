from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import OperationalError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import courier_required
from core.audit import client_ip
from orders.models import Order
from orders.services import transition


@login_required
@courier_required
def available_orders_view(request):
    orders = (
        Order.objects.filter(status='PENDING')
        .exclude(sender=request.user)
        .order_by('-created_at')[:50]
    )
    return render(request, 'couriers/available.html', {'orders': orders})


@login_required
@courier_required
def available_orders_json(request):
    orders = (
        Order.objects.filter(status='PENDING')
        .exclude(sender=request.user)
        .order_by('-created_at')[:50]
    )
    data = [
        {
            'id': o.id,
            'pickup_label': o.pickup_label,
            'dropoff_label': o.dropoff_label,
            'weight_kg': o.weight_kg,
            'item_type': o.item_type,
            'distance_km': o.distance_km,
            'predicted_fare': o.predicted_fare,
            'created_at': o.created_at.isoformat(),
        }
        for o in orders
    ]
    return JsonResponse(data, safe=False)


@login_required
@courier_required
@require_POST
def accept_order_view(request, pk):
    try:
        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=pk)
            except Order.DoesNotExist:
                messages.error(request, "Order does not exist.")
                return redirect('courier_available')

            if order.status != 'PENDING':
                messages.error(request, "Order was already taken.")
                return redirect('courier_available')

            if order.sender == request.user:
                messages.error(request, "You cannot accept your own order.")
                return redirect('courier_available')

            transition(order, 'ACCEPTED', actor=request.user, ip=client_ip(request))
            messages.success(request, f"Order #{order.id} accepted!")
            return redirect('courier_jobs')
    except OperationalError:
        messages.error(request, "Order was already taken.")
        return redirect('courier_available')


@login_required
@courier_required
@require_POST
def pickup_order_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.courier != request.user:
        raise PermissionDenied("Only the assigned courier can pick up this order.")

    transition(order, 'PICKED_UP', actor=request.user, ip=client_ip(request))
    messages.success(request, f"Order #{order.id} marked as picked up.")
    return redirect('courier_jobs')


@login_required
@courier_required
@require_POST
def deliver_order_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.courier != request.user:
        raise PermissionDenied("Only the assigned courier can deliver this order.")

    transition(order, 'DELIVERED', actor=request.user, ip=client_ip(request))
    messages.success(request, f"Order #{order.id} marked as delivered.")
    return redirect('courier_jobs')


@login_required
@courier_required
def my_jobs_view(request):
    jobs = Order.objects.filter(courier=request.user).order_by('-created_at')
    active_jobs = [j for j in jobs if j.status in ('ACCEPTED', 'PICKED_UP')]
    history_jobs = [j for j in jobs if j.status in ('DELIVERED', 'CANCELLED')]
    return render(
        request,
        'couriers/jobs.html',
        {
            'active_jobs': active_jobs,
            'history_jobs': history_jobs,
        },
    )

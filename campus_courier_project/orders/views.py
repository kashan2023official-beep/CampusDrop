from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from core.audit import client_ip, log
from .forms import OrderCreateForm
from .models import Order
from .services import transition
from .utils import CAMPUS_BOUNDS, CAMPUS_CENTER, compute_distance
from ml_engine.predictor import predict_fare


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'


class OrderCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderCreateForm
    template_name = 'orders/create.html'

    def form_valid(self, form):
        order = form.save(commit=False)
        order.sender = self.request.user
        order.distance_km = compute_distance(
            order.pickup_lat,
            order.pickup_lon,
            order.dropoff_lat,
            order.dropoff_lon,
        )
        
        hour = timezone.localtime().hour
        try:
            order.predicted_fare = predict_fare(
                order.distance_km, order.weight_kg, hour, order.item_type)
        except RuntimeError:
            order.predicted_fare = 0.0
            messages.warning(self.request, "Fare model not available. Fare will be calculated later.")
            
        order.save()
        log(
            actor=self.request.user,
            action="ORDER_CREATED",
            target_type="Order",
            target_id=order.id,
            metadata={"weight_kg": order.weight_kg, "distance_km": order.distance_km},
            ip=client_ip(self.request),
        )
        messages.success(self.request, f"Order #{order.id} created successfully!")
        return redirect('order_detail', pk=order.pk)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(sender=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order = super().get_object(queryset)
        user = self.request.user
        if not (user.is_staff or order.sender == user or order.courier == user):
            raise PermissionDenied("You do not have permission to view this order.")
        return order


@login_required
@require_POST
def order_cancel_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.sender != request.user:
        raise PermissionDenied("Only the sender can cancel this order.")
    if order.status not in {'PENDING', 'ACCEPTED'}:
        messages.error(request, f"Order cannot be cancelled in {order.status} status.")
        return redirect('order_detail', pk=order.pk)

    try:
        transition(order, 'CANCELLED', actor=request.user, ip=client_ip(request))
        messages.success(request, "Order has been cancelled.")
    except ValidationError as err:
        messages.error(request, str(err))

    return redirect('order_detail', pk=order.pk)


OrderCancelView = order_cancel_view


@login_required
def order_status_json(request, pk):
    order = get_object_or_404(Order, pk=pk)
    user = request.user
    if not (user.is_staff or order.sender == user or order.courier == user):
        raise PermissionDenied("Not permitted to view status.")

    data = {
        'id': order.id,
        'status': order.status,
        'courier': order.courier.username if order.courier else None,
        'accepted_at': order.accepted_at.isoformat() if order.accepted_at else None,
        'picked_up_at': order.picked_up_at.isoformat() if order.picked_up_at else None,
        'delivered_at': order.delivered_at.isoformat() if order.delivered_at else None,
    }
    return JsonResponse(data)


OrderStatusJSON = order_status_json


@login_required
def campus_bounds_view(request):
    data = {
        'center': list(CAMPUS_CENTER),
        'bounds': [
            [CAMPUS_BOUNDS['south'], CAMPUS_BOUNDS['west']],
            [CAMPUS_BOUNDS['north'], CAMPUS_BOUNDS['east']],
        ],
    }
    return JsonResponse(data)


CampusBoundsView = campus_bounds_view


@login_required
def distance_estimate_view(request):
    pickup_lat = request.GET.get('pickup_lat')
    pickup_lon = request.GET.get('pickup_lon')
    dropoff_lat = request.GET.get('dropoff_lat')
    dropoff_lon = request.GET.get('dropoff_lon')
    
    if None in (pickup_lat, pickup_lon, dropoff_lat, dropoff_lon):
        return JsonResponse({'error': 'Missing coordinates'}, status=400)
        
    try:
        distance_km = compute_distance(
            float(pickup_lat), float(pickup_lon),
            float(dropoff_lat), float(dropoff_lon)
        )
        return JsonResponse({'distance_km': distance_km})
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class ItemType(models.TextChoices):
    DOCUMENT = 'DOCUMENT', 'Document'
    FOOD = 'FOOD', 'Food'
    ELECTRONICS = 'ELECTRONICS', 'Electronics'
    CLOTHING = 'CLOTHING', 'Clothing'
    BOOKS = 'BOOKS', 'Books'
    OTHER = 'OTHER', 'Other'


class Status(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    PICKED_UP = 'PICKED_UP', 'Picked Up'
    DELIVERED = 'DELIVERED', 'Delivered'
    CANCELLED = 'CANCELLED', 'Cancelled'
class CancelReason(models.TextChoices):
    NO_COURIER = 'NO_COURIER', 'No Courier Available'
    CHANGE_OF_MIND = 'CHANGE_OF_MIND', 'Change of Mind'
    TOO_LATE = 'TOO_LATE', 'Taking Too Long'
    OTHER = 'OTHER', 'Other'


class Order(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_orders')
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='courier_orders')

    pickup_lat = models.FloatField()
    pickup_lon = models.FloatField()
    pickup_label = models.CharField(max_length=120, blank=True)

    dropoff_lat = models.FloatField()
    dropoff_lon = models.FloatField()
    dropoff_label = models.CharField(max_length=120, blank=True)

    weight_kg = models.FloatField(validators=[MinValueValidator(0.1)])
    item_type = models.CharField(max_length=40, choices=ItemType.choices)
    notes = models.TextField(blank=True)

    distance_km = models.FloatField(default=0.0)
    predicted_fare = models.FloatField(default=0.0)
    final_fare = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    cancel_reason = models.CharField(max_length=20, choices=CancelReason.choices, blank=True)
    cancel_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['sender']),
            models.Index(fields=['courier']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Order #{self.id} [{self.status}]"

    def contact_visible(self):
        return self.status in {Status.ACCEPTED, Status.PICKED_UP, Status.DELIVERED}

    def can_be_rated_by(self, user):
        if self.status != Status.DELIVERED:
            return False
        if user not in (self.sender, self.courier):
            return False
        return not Rating.objects.filter(order=self, rater=user).exists()


class Rating(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    stars = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('order', 'rater')

    def __str__(self):
        return f"{self.stars} stars by {self.rater.username} on Order #{self.order.id}"

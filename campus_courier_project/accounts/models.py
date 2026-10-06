from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_courier = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    rating = models.FloatField(default=5.0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def update_rating(self, new_stars):
        if self.rating_count == 0:
            self.rating = float(new_stars)
            self.rating_count = 1
        else:
            total_stars = (self.rating * self.rating_count) + new_stars
            self.rating_count += 1
            self.rating = total_stars / self.rating_count
        self.save(update_fields=['rating', 'rating_count'])

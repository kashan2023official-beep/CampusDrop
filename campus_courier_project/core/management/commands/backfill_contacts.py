from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = "Backfill blank emails and phone numbers for users and profiles."

    def handle(self, *args, **options):
        users_updated = 0
        profiles_updated = 0

        # Backfill emails
        for user in User.objects.filter(email=''):
            user.email = f"{user.username}@uet.edu.pk"
            user.save(update_fields=['email'])
            users_updated += 1

        # Backfill phones
        for profile in Profile.objects.filter(phone=''):
            # Zero-pad ID to 9 digits, e.g., id=1 -> "000000001", then prepend "03"
            # Format: 03 + 9 digits = 11 digits total.
            padded_id = f"{profile.id:09d}"
            profile.phone = f"03{padded_id}"
            profile.save(update_fields=['phone'])
            profiles_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{users_updated} users updated, {profiles_updated} profiles updated."
            )
        )

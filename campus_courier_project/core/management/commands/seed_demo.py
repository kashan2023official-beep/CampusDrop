from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from orders.models import Order, ItemType, Status
from orders.utils import compute_distance
from core.audit import log


class Command(BaseCommand):
    help = "Seed demo data: users, courier profile, sample orders across campus, and audit logs."

    def handle(self, *args, **options):
        if User.objects.filter(username='demo_sender').exists():
            self.stdout.write(
                self.style.WARNING("Warning: User 'demo_sender' already exists. Skipping seed_demo (idempotent).")
            )
            return

        self.stdout.write("Seeding demo data...")

        # 1. Create demo_sender
        demo_sender = User.objects.create_user(
            username='demo_sender',
            email='demo.sender@uet.edu.pk',
            password='DemoPass123!',
            first_name='Demo',
            last_name='Sender',
        )
        demo_sender.profile.phone = '03001234501'
        demo_sender.profile.save()

        # 2. Create demo_courier with is_courier=True
        demo_courier = User.objects.create_user(
            username='demo_courier',
            email='demo.courier@uet.edu.pk',
            password='DemoPass123!',
            first_name='Demo',
            last_name='Courier',
        )
        demo_courier.profile.is_courier = True
        demo_courier.profile.phone = '03001234502'
        demo_courier.profile.save()

        # 3. Create demo_admin (staff + superuser)
        demo_admin = User.objects.create_superuser(
            username='demo_admin',
            email='demo.admin@uet.edu.pk',
            password='DemoPass123!',
            first_name='Demo',
            last_name='Admin',
        )
        demo_admin.profile.phone = '03001234503'
        demo_admin.profile.save()

        users_created = 3

        now = timezone.now()

        # 4. Create 6 orders inside campus bounds with diverse item types & statuses
        # Campus bounds: S: 31.5757, N: 31.5838, W: 74.3507, E: 74.3592
        orders_data = [
            {
                'pickup_lat': 31.5760,
                'pickup_lon': 74.3510,
                'pickup_label': 'Main Gate (GT Road)',
                'dropoff_lat': 31.5790,
                'dropoff_lon': 74.3530,
                'dropoff_label': 'Computer Science Department',
                'weight_kg': 0.5,
                'item_type': ItemType.DOCUMENT,
                'notes': 'Urgent departmental documents. Please deliver to Room 204.',
                'status': Status.PENDING,
                'courier': None,
                'predicted_fare': 120.0,
                'accepted_at': None,
                'picked_up_at': None,
                'delivered_at': None,
            },
            {
                'pickup_lat': 31.5770,
                'pickup_lon': 74.3520,
                'pickup_label': 'Administration Block',
                'dropoff_lat': 31.5810,
                'dropoff_lon': 74.3550,
                'dropoff_label': 'Electrical Engineering Dept',
                'weight_kg': 1.2,
                'item_type': ItemType.FOOD,
                'notes': 'Lunch box package. Keep upright.',
                'status': Status.ACCEPTED,
                'courier': demo_courier,
                'predicted_fare': 150.0,
                'accepted_at': now,
                'picked_up_at': None,
                'delivered_at': None,
            },
            {
                'pickup_lat': 31.5780,
                'pickup_lon': 74.3530,
                'pickup_label': 'Central Library',
                'dropoff_lat': 31.5825,
                'dropoff_lon': 74.3560,
                'dropoff_label': 'Hostel 5 (Fatima Hall)',
                'weight_kg': 2.5,
                'item_type': ItemType.ELECTRONICS,
                'notes': 'Laptop charger and testing equipment. Fragile.',
                'status': Status.PICKED_UP,
                'courier': demo_courier,
                'predicted_fare': 220.0,
                'accepted_at': now,
                'picked_up_at': now,
                'delivered_at': None,
            },
            {
                'pickup_lat': 31.5775,
                'pickup_lon': 74.3540,
                'pickup_label': 'Student Center & Cafeteria',
                'dropoff_lat': 31.5805,
                'dropoff_lon': 74.3515,
                'dropoff_label': 'Mechanical Engineering Dept',
                'weight_kg': 1.8,
                'item_type': ItemType.CLOTHING,
                'notes': 'Society event t-shirts parcel.',
                'status': Status.DELIVERED,
                'courier': demo_courier,
                'predicted_fare': 180.0,
                'final_fare': 180.0,
                'accepted_at': now,
                'picked_up_at': now,
                'delivered_at': now,
            },
            {
                'pickup_lat': 31.5795,
                'pickup_lon': 74.3525,
                'pickup_label': 'Chemistry Department',
                'dropoff_lat': 31.5765,
                'dropoff_lon': 74.3535,
                'dropoff_label': 'Medical Center',
                'weight_kg': 0.8,
                'item_type': ItemType.BOOKS,
                'notes': 'Medical reference books. Cancelled by sender.',
                'status': Status.CANCELLED,
                'courier': None,
                'predicted_fare': 130.0,
                'accepted_at': None,
                'picked_up_at': None,
                'delivered_at': None,
            },
            {
                'pickup_lat': 31.5810,
                'pickup_lon': 74.3555,
                'pickup_label': 'Auditorium Complex',
                'dropoff_lat': 31.5835,
                'dropoff_lon': 74.3570,
                'dropoff_label': 'Sports Complex & Gymnasium',
                'weight_kg': 3.0,
                'item_type': ItemType.OTHER,
                'notes': 'Sports kit and tournament stopwatch.',
                'status': Status.PENDING,
                'courier': None,
                'predicted_fare': 250.0,
                'accepted_at': None,
                'picked_up_at': None,
                'delivered_at': None,
            },
        ]

        orders_created = 0
        for o_data in orders_data:
            dist = compute_distance(
                o_data['pickup_lat'],
                o_data['pickup_lon'],
                o_data['dropoff_lat'],
                o_data['dropoff_lon'],
            )

            order = Order.objects.create(
                sender=demo_sender,
                courier=o_data['courier'],
                pickup_lat=o_data['pickup_lat'],
                pickup_lon=o_data['pickup_lon'],
                pickup_label=o_data['pickup_label'],
                dropoff_lat=o_data['dropoff_lat'],
                dropoff_lon=o_data['dropoff_lon'],
                dropoff_label=o_data['dropoff_label'],
                weight_kg=o_data['weight_kg'],
                item_type=o_data['item_type'],
                notes=o_data['notes'],
                distance_km=dist,
                predicted_fare=o_data['predicted_fare'],
                final_fare=o_data.get('final_fare'),
                status=o_data['status'],
                accepted_at=o_data.get('accepted_at'),
                picked_up_at=o_data.get('picked_up_at'),
                delivered_at=o_data.get('delivered_at'),
            )
            orders_created += 1

            # Log audit entry for the order
            log(
                actor=demo_sender,
                action=f"ORDER_{order.status}",
                target_type='Order',
                target_id=order.id,
                metadata={'status': order.status, 'seed': True, 'item_type': order.item_type},
                ip='127.0.0.1',
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completed successfully: {users_created} users created, {orders_created} orders created."
            )
        )

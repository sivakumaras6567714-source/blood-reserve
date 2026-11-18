from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from directory.models import BloodGroup, Donor

class Command(BaseCommand):
    help = "Create fictional demo blood groups and donors"
    def handle(self, *args, **kwargs):
        for name in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            BloodGroup.objects.get_or_create(name=name)
        samples = [
            ("Arun Kumar", 27, "O+", "Coimbatore", 130),
            ("Meena R", 24, "A+", "Coimbatore", 220),
            ("Karthik S", 31, "B+", "Chennai", 40),
            ("Divya M", 29, "O-", "Coimbatore", 105),
            ("Rahul P", 26, "AB+", "Tiruppur", None),
        ]
        for name, age, group, city, days in samples:
            last = timezone.localdate() - timedelta(days=days) if days else None
            Donor.objects.get_or_create(name=name, city=city, blood_group=BloodGroup.objects.get(name=group),
                defaults={"age": age, "phone": "9000000000", "last_donation_date": last, "is_verified": True})
        self.stdout.write(self.style.SUCCESS("Demo data ready. All sample people/details are fictional."))

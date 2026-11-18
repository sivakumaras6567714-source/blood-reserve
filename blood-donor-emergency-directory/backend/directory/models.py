from django.db import models
from django.utils import timezone
from datetime import timedelta

class BloodGroup(models.Model):
    name = models.CharField(max_length=3, unique=True)
    def __str__(self): return self.name

class HospitalAccount(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=160)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Donor(models.Model):
    name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField()
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT, related_name="donors")
    city = models.CharField(max_length=120)
    phone = models.CharField(max_length=25)
    email = models.EmailField(blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    consent_to_contact = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def eligible_by_90_day_rule(self):
        return not self.last_donation_date or self.last_donation_date <= timezone.localdate() - timedelta(days=90)

    def __str__(self): return f"{self.name} ({self.blood_group})"

class DonationRecord(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name="donation_records")
    donation_date = models.DateField()
    location = models.CharField(max_length=160, blank=True)
    notes = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-donation_date"]

class EmergencyRequest(models.Model):
    URGENCY = [("critical", "Critical"), ("urgent", "Urgent"), ("normal", "Normal")]
    requester_name = models.CharField(max_length=120)
    requester_phone = models.CharField(max_length=25)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT)
    city = models.CharField(max_length=120)
    hospital_name = models.CharField(max_length=160)
    units_needed = models.PositiveSmallIntegerField(default=1)
    urgency = models.CharField(max_length=10, choices=URGENCY, default="urgent")
    details = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

class ContactRequest(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name="contact_requests")
    emergency_request = models.ForeignKey(EmergencyRequest, on_delete=models.CASCADE, related_name="contact_requests")
    message = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

class VerificationBadge(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name="badges", null=True, blank=True)
    hospital = models.ForeignKey(HospitalAccount, on_delete=models.CASCADE, related_name="badges", null=True, blank=True)
    label = models.CharField(max_length=80, default="Identity checked")
    verified_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): return self.label

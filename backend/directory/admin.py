from django.contrib import admin
from .models import BloodGroup, Donor, DonationRecord, EmergencyRequest, HospitalAccount, VerificationBadge, ContactRequest

admin.site.register(BloodGroup)
admin.site.register(Donor)
admin.site.register(DonationRecord)
admin.site.register(EmergencyRequest)
admin.site.register(HospitalAccount)
admin.site.register(VerificationBadge)
admin.site.register(ContactRequest)

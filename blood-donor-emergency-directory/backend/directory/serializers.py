from rest_framework import serializers
from .models import BloodGroup, Donor, EmergencyRequest, ContactRequest

class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = ["id", "name"]

class DonorSerializer(serializers.ModelSerializer):
    blood_group = serializers.SlugRelatedField(slug_field="name", queryset=BloodGroup.objects.all())
    eligible = serializers.BooleanField(source="eligible_by_90_day_rule", read_only=True)
    class Meta:
        model = Donor
        fields = ["id", "name", "age", "blood_group", "city", "last_donation_date", "is_verified", "eligible"]
        # Private contact information is deliberately excluded.

class DonorCreateSerializer(serializers.ModelSerializer):
    blood_group = serializers.SlugRelatedField(slug_field="name", queryset=BloodGroup.objects.all())
    class Meta:
        model = Donor
        fields = ["name", "age", "blood_group", "city", "phone", "email", "last_donation_date", "consent_to_contact"]

class EmergencyRequestSerializer(serializers.ModelSerializer):
    blood_group = serializers.SlugRelatedField(slug_field="name", queryset=BloodGroup.objects.all())
    class Meta:
        model = EmergencyRequest
        fields = ["id", "requester_name", "requester_phone", "blood_group", "city", "hospital_name",
                  "units_needed", "urgency", "details", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ["id", "donor", "emergency_request", "message", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BloodGroup, Donor, EmergencyRequest, ContactRequest
from .serializers import (BloodGroupSerializer, DonorSerializer, DonorCreateSerializer,
                          EmergencyRequestSerializer, ContactRequestSerializer)

class BloodGroupList(generics.ListAPIView):
    queryset = BloodGroup.objects.all().order_by("name")
    serializer_class = BloodGroupSerializer

class DonorList(generics.ListAPIView):
    serializer_class = DonorSerializer
    def get_queryset(self):
        qs = Donor.objects.select_related("blood_group").filter(consent_to_contact=True)
        group = self.request.query_params.get("blood_group")
        city = self.request.query_params.get("location")
        eligible = self.request.query_params.get("eligible", "true").lower()
        if group: qs = qs.filter(blood_group__name=group)
        if city: qs = qs.filter(city__icontains=city)
        if eligible == "true":
            cutoff = timezone.localdate() - timedelta(days=90)
            qs = qs.filter(Q(last_donation_date__isnull=True) | Q(last_donation_date__lte=cutoff))
        return qs.order_by("-is_verified", "name")

class DonorCreate(generics.CreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorCreateSerializer

class EmergencyRequestCreate(generics.CreateAPIView):
    queryset = EmergencyRequest.objects.all()
    serializer_class = EmergencyRequestSerializer

class ContactRequestCreate(generics.CreateAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "Blood Donor Emergency Directory"})

@api_view(["GET"])
def stats(request):
    cutoff = timezone.localdate() - timedelta(days=90)
    donors = Donor.objects.all()
    return Response({
        "total_donors": donors.count(),
        "eligible_donors": donors.filter(Q(last_donation_date__isnull=True) | Q(last_donation_date__lte=cutoff)).count(),
        "open_requests": EmergencyRequest.objects.filter(status="open").count(),
    })

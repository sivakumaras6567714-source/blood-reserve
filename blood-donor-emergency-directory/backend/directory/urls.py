from django.urls import path
from .views import BloodGroupList, DonorList, DonorCreate, EmergencyRequestCreate, ContactRequestCreate, health, stats

urlpatterns = [
    path("health/", health),
    path("stats/", stats),
    path("blood-groups/", BloodGroupList.as_view()),
    path("donors/", DonorList.as_view()),
    path("donors/register/", DonorCreate.as_view()),
    path("emergency-requests/", EmergencyRequestCreate.as_view()),
    path("contact-requests/", ContactRequestCreate.as_view()),
]

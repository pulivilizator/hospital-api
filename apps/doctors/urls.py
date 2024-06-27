from rest_framework.routers import DefaultRouter

from apps.doctors.views import DoctorViewSet, ServiceViewSet

router = DefaultRouter()

router.register('doctors', DoctorViewSet, basename='doctor')
router.register('services', ServiceViewSet, basename='service')
from django.urls import re_path, include

from apps.accounts.urls import v1_urlpatterns as v1_accounts_urls
from apps.doctors.urls import router as doctors_router

v1_urlpatterns = [
    re_path(r'', include(v1_accounts_urls)),
    re_path(r'', include(doctors_router.urls)),
]
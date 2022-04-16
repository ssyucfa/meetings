from django.urls import path, include
from rest_framework.routers import SimpleRouter

from meetings.views import UserViewSet

router = SimpleRouter()
router.register(r'clients', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

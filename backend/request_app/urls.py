from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RequestViewSet

router = DefaultRouter()
router.register(r'requests', RequestViewSet, 'requests')


urlpatterns = [
    path('', include(router.urls), name="requests")
]

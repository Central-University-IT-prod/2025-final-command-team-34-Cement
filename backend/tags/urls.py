from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename="tags")

app_name = "tags"

urlpatterns = [
    path('', include(router.urls))
]

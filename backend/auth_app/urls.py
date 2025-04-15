from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import AuthViewSet, UsersAPIView, UpdatePasswordAPIView, SetRatingView, RatingView, RetrieveUserAPIView, UploadImageView

auth_router = SimpleRouter()
auth_router.register("auth", AuthViewSet, "auth")

urlpatterns = [
    path('mentors/<str:login>/rating', RatingView.as_view()),
    path('users/me/', UsersAPIView.as_view()),
    path('users/change_password/', UpdatePasswordAPIView.as_view()),
    path('set-rating/<str:login>/', SetRatingView.as_view()),
    path('users/<str:login>/', RetrieveUserAPIView.as_view()),
    path('add-image/', UploadImageView.as_view()),
    path('', include(auth_router.urls)),
]

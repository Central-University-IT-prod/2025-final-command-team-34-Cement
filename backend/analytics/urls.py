from django.urls import path
from .views import AnalyticsViewSet

urlpatterns = [
    path('analytics/mentors/tags/', AnalyticsViewSet.as_view({'get': 'get_tag_stats'}), name='analytics-mentors-tags'),
    path('analytics/count/', AnalyticsViewSet.as_view({'get': 'get_count'}), name='analytics-count'),
    path('analytics/mentors/stats/', AnalyticsViewSet.as_view({'get': 'get_top_mentors'}), name='analytics-mentors-stats'),
    path('analytics/requests/stats/', AnalyticsViewSet.as_view({'get': 'get_requests_stats'}), name='requests-stats'),
]
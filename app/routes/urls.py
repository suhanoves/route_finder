from django.urls import path

from routes.views import Homepage, FoundRoutesView, RoutesListView

app_name = 'routes'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('found_routes/', FoundRoutesView.as_view(), name='found_routes'),
    path('routes/', RoutesListView.as_view(), name='routes'),
]

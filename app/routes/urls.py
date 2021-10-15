from django.urls import path

from routes.views import Homepage, FoundRoutesView, RoutesListView, CreateRouteView

app_name = 'routes'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('found_routes/', FoundRoutesView.as_view(), name='found_routes'),
    path('routes/create_route', CreateRouteView.as_view(), name='create_route'),
    path('routes/', RoutesListView.as_view(), name='routes'),
]

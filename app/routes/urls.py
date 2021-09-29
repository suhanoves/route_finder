from django.urls import path

from routes.views import RouteSearchFormView, FoundRoutesView, RoutesListView

app_name = 'routes'

urlpatterns = [
    path('', RouteSearchFormView.as_view(), name='route_search'),
    path('found_routes/', FoundRoutesView.as_view(), name='found_routes'),
    path('routes/', RoutesListView.as_view(), name='routes'),
]

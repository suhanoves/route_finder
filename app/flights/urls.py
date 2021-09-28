from django.urls import path

from flights.views import *

app_name = 'flights'

urlpatterns = [
    path('', FlightsListView.as_view(), name='flights'),
    path('<int:pk>', FlightDetailView.as_view(), name='flight'),
    path('create/', FlightCreateView.as_view(), name='flight_create'),
    path('<int:pk>/update/', FlightUpdateView.as_view(), name='flight_update'),
    path('<int:pk>/delete/', FlightDeleteView.as_view(), name='flight_delete'),
]

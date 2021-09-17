from django.urls import path

from cities.views import *

app_name = 'cities'

urlpatterns = [
    path('', CitiesListView.as_view(), name='cities'),
    path('<int:pk>', CityDetailView.as_view(), name='city'),
    path('create/', CityCreateView.as_view(), name='city_create'),
    path('<int:pk>/update/', CityUpdateView.as_view(), name='city_update'),
    path('<int:pk>/delete/', CityDeleteView.as_view(), name='city_delete'),
]

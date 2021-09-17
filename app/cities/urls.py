from django.urls import path

from cities.views import *

app_name = 'cities'

urlpatterns = [
    path('', CitiesListView.as_view(), name='cities'),
    path('city/<int:pk>', CityDetailView.as_view(), name='city')
]

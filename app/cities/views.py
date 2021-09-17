from django.views.generic import ListView, DetailView

from cities.models import City

__all__ = (
    'CitiesListView',
    'CityDetailView'
)


class CitiesListView(ListView):
    model = City


class CityDetailView(DetailView):
    model = City

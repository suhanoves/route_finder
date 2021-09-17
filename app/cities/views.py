from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cities.models import City

__all__ = (
    'CitiesListView',
    'CityDetailView',
    'CityCreateView',
    'CityUpdateView',
    'CityDeleteView',
)


class CitiesListView(ListView):
    model = City


class CityDetailView(DetailView):
    model = City


class CityCreateView(CreateView):
    model = City
    fields = ['name']
    success_url = reverse_lazy('cities:cities')


class CityUpdateView(UpdateView):
    model = City
    fields = ['name']


class CityDeleteView(DeleteView):
    model = City
    success_url = reverse_lazy('cities:cities')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

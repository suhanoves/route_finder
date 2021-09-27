from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

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


class CityFormView(SuccessMessageMixin):
    model = City
    fields = ['name']
    success_url = reverse_lazy('cities:cities')

    def get_success_message(self, cleaned_data):
        success_message = super().get_success_message(cleaned_data)
        return messages.success(self.request, success_message, extra_tags='success')


class CityCreateView(CityFormView, CreateView):
    success_message = f"Город %(name)s добавлен"


class CityUpdateView(CityFormView, UpdateView):
    success_message = f"Город %(name)s отредактирован успешно"


class CityDeleteView(SuccessMessageMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities:cities')
    success_message = f"Город %(name)s удалён"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__, extra_tags='danger')
        return super().delete(request, *args, **kwargs)

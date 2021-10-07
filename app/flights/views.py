from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, \
    UpdateView

from flights.models import Flight

__all__ = (
    'FlightsListView',
    'FlightDetailView',
    'FlightCreateView',
    'FlightUpdateView',
    'FlightDeleteView',
)


class FlightsListView(ListView):
    model = Flight
    queryset = Flight.objects.select_related()
    paginate_by = 13


class FlightDetailView(DetailView):
    model = Flight
    queryset = Flight.objects.select_related()


class FlightFormView(SuccessMessageMixin, View):
    model = Flight
    fields = [
        'number',
        'duration',
        'price',
        'origin',
        'destination',
    ]
    success_url = reverse_lazy('flights:flights')

    def get_success_message(self, cleaned_data):
        success_message = super().get_success_message(cleaned_data)
        return messages.success(self.request, success_message,
                                extra_tags='success')


class FlightCreateView(FlightFormView, CreateView):
    success_message = f"Рейс %(origin)s — %(destination)s добавлен"


class FlightUpdateView(FlightFormView, UpdateView):
    success_message = (f"Рейс %(origin)s — %(destination)s "
                       f"отредактирован успешно")


class FlightDeleteView(SuccessMessageMixin, DeleteView):
    model = Flight
    success_url = reverse_lazy('flights:flights')
    success_message = f"Рейс %(origin)s — %(destination)s удалён"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__,
                         extra_tags='danger')
        return super().delete(request, *args, **kwargs)

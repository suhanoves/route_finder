from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from routes.forms import RouteSearchForm


class RouteSearchFormView(FormView):
    form_class = RouteSearchForm
    template_name = 'routes/route_search.html'
    success_url = reverse_lazy('routes:found_routes')


# Create your views here.

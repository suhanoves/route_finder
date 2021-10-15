from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, FormMixin, CreateView

from routes.forms import RouteSearchForm
from routes.models import Route
from routes.services.route_finder import route_finder


class Homepage(FormMixin, TemplateView):
    form_class = RouteSearchForm
    template_name = 'routes/homepage.html'


class FoundRoutesView(FormView):
    form_class = RouteSearchForm
    template_name = 'routes/found_routes.html'

    def form_valid(self, form):
        routes = route_finder(form)
        self.object_list = routes
        context = {'form': form, 'routes': routes}
        return super().render_to_response(context)


class CreateRouteView(CreateView):
    model = Route
    fields = ('name', 'duration', 'price', 'origin', 'destination', 'flights',)
    success_url = reverse_lazy('routes:found_routes')


class RoutesListView(ListView):
    pass

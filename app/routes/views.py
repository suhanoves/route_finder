from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, FormMixin

from routes.forms import RouteSearchForm
from routes.services.route_finder import route_finder


class Homepage(FormMixin, TemplateView):
    form_class = RouteSearchForm
    template_name = 'routes/homepage.html'


class FoundRoutesView(FormView):
    form_class = RouteSearchForm
    template_name = 'routes/found_routes.html'

    def form_valid(self, form):
        self.extra_context = route_finder(self.request, form)
        return super().form_valid(form)
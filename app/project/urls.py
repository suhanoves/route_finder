"""project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # My urls
    path('',
         RedirectView.as_view(pattern_name='cities:cities'),
         name='homepage'
         ),
    path('cities/', include('cities.urls')),
    path('flights/', include('flights.urls')),

    # Django urls
    path('admin/', admin.site.urls),
]

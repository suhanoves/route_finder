"""project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # My urls
    path('', include('routes.urls')),
    path('cities/', include('cities.urls')),
    path('flights/', include('flights.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Django urls
    path('admin/', admin.site.urls),
]

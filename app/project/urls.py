"""project URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # My urls
    path('', include('routes.urls')),
    path('cities/', include('cities.urls')),
    path('flights/', include('flights.urls')),
    path('accounts/', include('accounts.urls')),

    # Django urls
    path('admin/', admin.site.urls),
]

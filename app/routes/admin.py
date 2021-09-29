from django.contrib import admin

from routes.models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'origin',
        'destination',
        'duration',
        'price',
    )
    search_fields = (
        'name',
        'origin',
        'destination',
    )
    list_filter = (
        'origin',
        'destination'
    )

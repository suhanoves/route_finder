from django.contrib import admin

from flights.models import Flight


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    ordering = ['origin', 'destination']
    list_display = ['number', 'origin', 'destination', 'duration', ]
    search_fields = ['origin', 'destination']

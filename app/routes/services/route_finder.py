from itertools import groupby
from typing import List, Dict

from django.http import HttpRequest

from cities.models import City
from flights.models import Flight
from routes.forms import RouteSearchForm


def find_path_dfs(graph, origin: City, destination: City):
    stack = [(origin, [origin])]

    while stack:
        city, path = stack.pop()
        neighbors = graph[city]
        for neighbor in neighbors:
            if neighbor not in path:
                if neighbor == destination:
                    yield path + [neighbor]
                else:
                    stack.append((neighbor, path + [neighbor]))


def make_adjacency_graph(flights: List[Flight]) -> Dict[City, List[City]]:
    """
    Make an adjacency list representation of a graph from a list of graph edges
    where vertices are Cities and edges are Flights
    """
    sorted_flights = sorted(flights, key=lambda flight: flight.origin)
    group_flights = groupby(sorted_flights, lambda flight: flight.origin)
    adjacency_list = {
        city: [flight.destination for flight in flights] for city, flights in group_flights
    }
    return adjacency_list


def route_finder(request: HttpRequest, form: RouteSearchForm) -> List:
    origin = form.cleaned_data['origin']
    destination = form.cleaned_data['destination']
    transfers = form.cleaned_data['transfers']
    price_limit = form.cleaned_data['price_limit']
    duration_limit = form.cleaned_data['duration_limit']

    flights = Flight.objects.all()

    graph = make_adjacency_graph(flights)
    routes = find_path_dfs(graph, origin, destination)

    if transfers:
        routes = filter(
            lambda path: set(transfers).issubset(set(path)),
            routes
        )
    return list(routes)

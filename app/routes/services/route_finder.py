from dataclasses import dataclass, field
from datetime import timedelta
from decimal import Decimal
from itertools import groupby
from typing import List, Dict, Generator, Tuple, Set

from cities.models import City
from flights.models import Flight
from routes.forms import RouteSearchForm


@dataclass
class FoundRoute:
    """
    A class represents a route between two cities and includes
    all waypoints and flights that are required for this route,
    total duration and cost of the route.
    """

    waypoints: List[City] = field(default_factory=list)
    flights: List[Flight] = field(default_factory=list)
    duration: timedelta = timedelta()
    price: Decimal = Decimal()


def make_adjacency_graph(flights: List[Flight]) -> Dict[City, List[Tuple[City, Flight]]]:
    """
    Convert representation of a weighted graph from a list of edges to the adjacency list
    City_origin: [(City_destination, Flight), ]
    """
    sorted_flights = sorted(flights, key=lambda flight: flight.origin)
    group_flights = groupby(sorted_flights, lambda flight: flight.origin)
    adjacency_list = {
        city: [(flight.destination, flight) for flight in flights] for city, flights in group_flights
    }
    return adjacency_list


def find_routes_dfs(graph, origin: City, destination: City) -> Generator:
    """Finds all possible routes from origin to destination using DFS"""

    stack = [(origin, FoundRoute(waypoints=[origin]))]

    while stack:
        city, route = stack.pop()
        neighbors = graph[city]
        for neighbor, flight in neighbors:
            if neighbor not in route.waypoints:
                if neighbor == destination:
                    waypoints = route.waypoints + [neighbor]
                    flights = route.flights + [flight]
                    duration = sum((flight.duration for flight in flights), timedelta())
                    price = sum(flight.price for flight in flights)

                    yield FoundRoute(waypoints=waypoints,
                                     flights=flights,
                                     duration=duration,
                                     price=price)
                else:
                    stack.append(
                        (neighbor,
                         FoundRoute(
                             waypoints=route.waypoints + [neighbor],
                             flights=route.flights + [flight]
                         ))
                    )


def apply_transfers_filter(routes, transfers: Set[City]):
    filtered_routes = routes
    if transfers:
        filtered_routes = filter(
            lambda route: set(transfers).issubset(set(route.waypoints)),
            routes
        )
    return filtered_routes


def apply_duration_filter(routes, duration_limit: timedelta):
    filtered_routes = routes
    if duration_limit:
        filtered_routes = filter(
            lambda route: route.duration < duration_limit,
            routes
        )
    return filtered_routes


def apply_price_filter(routes, price_limit: Decimal):
    filtered_routes = routes
    if price_limit:
        filtered_routes = filter(
            lambda route: route.price < price_limit,
            routes
        )
    return filtered_routes


def route_finder(form: RouteSearchForm) -> Dict[str, list]:
    origin = form.cleaned_data['origin']
    destination = form.cleaned_data['destination']
    transfers = form.cleaned_data['transfers']
    price_limit = form.cleaned_data['price_limit']
    duration_limit = form.cleaned_data['duration_limit']

    flights = Flight.objects.select_related('origin', 'destination')

    graph = make_adjacency_graph(flights)
    routes = find_routes_dfs(graph, origin, destination)

    routes = apply_transfers_filter(routes, transfers)
    routes = apply_duration_filter(routes, duration_limit)
    routes = apply_price_filter(routes, price_limit)

    routes = list(routes)

    return routes

from itertools import tee
from datetime import date, datetime
from geopy import distance


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def compute_distance(point1, point2):
    """
    :type point1: structures.Coords
    :type point2: structures.Coords
    :return: Distance
    """
    return distance.geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).m


# def compute_distance(point1, point2):
#     return ((point1.x_utm - point2.x_utm) ** 2 + (point1.y_utm - point2.y_utm) ** 2) ** 0.5


def current_weekday():
    return date.today().strftime('%A')


def current_hour():
    return datetime.today().strftime('%H')

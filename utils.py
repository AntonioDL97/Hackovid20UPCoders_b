from itertools import tee
from datetime import date, datetime


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def compute_distance(point1, point2):
    return ((point1.x_utm - point2.x_utm) ** 2 + (point1.y_utm - point2.y_utm) ** 2) ** 0.5


def current_weekday():
    return date.today().strftime('%A')


def current_hour():
    return datetime.today().strftime('%H')

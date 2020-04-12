from typing import Union


class Address:
    def __init__(self, name: str, street: str, num: int):
        self.name = name
        self.street = street
        self.num = num

    def __hash__(self):
        return hash(tuple(self.__dict__.values()))

    def __eq__(self, other):
        return isinstance(other, Address) and self.name == other.name and \
               self.street == other.street and self.num == other.num

    def __repr__(self):
        return f'{self.name.title()} ({self.street.title()}, {self.num})'

    def to_dict(self):
        return dict(name=self.name, street=self.street, num=self.num)


class Coords:
    def __init__(self, latitude: float = None, longitude: float = None, x_utm: float = None, y_utm: float = None):
        self.latitude = latitude
        self.longitude = longitude
        self.x_utm = x_utm
        self.y_utm = y_utm

    def to_dict(self):
        return dict(latitude=self.latitude, longitude=self.longitude, x_utm=self.x_utm, y_utm=self.y_utm)


class Shop:
    def __init__(self, identifier: Union[int, str], activity: str = None, coords: Coords = None,
                 address: Address = None):
        self.identifier = identifier
        self.activity = activity
        self.address = address
        self.coords = coords
        self.gmaps_id = None
        self.pct_people = 0
        self.is_open = True
        self.rating = 0

    def __repr__(self):
        return str(self.address)

    def set_gmaps_info(self, gmaps_id: int, is_open: bool, rating: int):
        self.gmaps_id = gmaps_id
        self.is_open = is_open
        self.rating = rating

    def set_pct_people(self, pct_people: int):
        self.pct_people = pct_people

    def to_dict(self):
        return dict(activity=self.activity,
                    gmaps_id=self.gmaps_id,
                    coords=self.coords.to_dict(),
                    address=self.address.to_dict())
